// Canonical artwork is authored data in work/scenes.json (scene visual objects/actions).
// review-revision/art.mjs is a superseded five-scene generator kept for history only;
// importing it would overwrite the reviewed four-scene staging, so this entry point
// only validates the canonical data and prints its art hash.
import fs from 'node:fs';import crypto from 'node:crypto';
const scenes=JSON.parse(fs.readFileSync(new URL('work/scenes.json',import.meta.url)));
if(scenes.length!==4||scenes.some(s=>!s.visual?.objects?.length))throw Error('work/scenes.json must hold the four authored scene visuals.');
console.log('artSha256',crypto.createHash('sha256').update(JSON.stringify(scenes.map(s=>({id:s.id,visual:s.visual})))).digest('hex'));
