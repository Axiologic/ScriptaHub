import { spawn } from 'node:child_process';

export function assertNodeVersion(version = process.versions.node, command = 'ScriptaHub tools') {
    const [major, minor] = version.split('.').map(Number);
    if (!Number.isInteger(major) || !Number.isInteger(minor) || major < 22 || (major === 22 && minor < 12)) {
        throw new Error(`${command} requires Node.js 22.12 or newer; found ${version}. Install a supported Node.js release using the instructions in dependencies.md.`);
    }
}

export function runProcess(command, args, { input, timeout = 30000, cwd, env = process.env, maxBytes = 32 * 1024 * 1024 } = {}) {
    return new Promise((resolve, reject) => {
        const child = spawn(command, args, { cwd, env, stdio: ['pipe', 'pipe', 'pipe'] });
        const stdout = [];
        const stderr = [];
        let bytes = 0;
        let settled = false;
        const abort = (error) => {
            if (settled) return;
            settled = true;
            clearTimeout(timer);
            child.kill('SIGKILL');
            // Descendants may inherit pipes; do not wait for their handles to close.
            child.stdin.destroy();
            child.stdout.destroy();
            child.stderr.destroy();
            reject(error);
        };
        const timer = setTimeout(() => abort(new Error(`${command} exceeded its ${timeout} ms time limit.`)), timeout);
        const collect = (target) => (chunk) => {
            bytes += chunk.length;
            if (bytes > maxBytes) {
                abort(new Error(`${command} exceeded its output limit.`));
            } else {
                target.push(chunk);
            }
        };
        child.stdout.on('data', collect(stdout));
        child.stderr.on('data', collect(stderr));
        child.on('error', (error) => {
            if (settled) return;
            settled = true;
            clearTimeout(timer);
            reject(error);
        });
        child.on('close', (code, signal) => {
            if (settled) return;
            settled = true;
            clearTimeout(timer);
            resolve({ code, signal, stdout: Buffer.concat(stdout).toString('utf8'), stderr: Buffer.concat(stderr).toString('utf8') });
        });
        child.stdin.on('error', (error) => {
            if (error.code !== 'EPIPE') {
                abort(error);
            }
        });
        child.stdin.end(input);
    });
}
