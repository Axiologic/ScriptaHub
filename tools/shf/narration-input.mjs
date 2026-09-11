import {createHash} from 'node:crypto';

export function narrationDirection(scene,index,production){
  const emotion=scene.emotionalPlan?.states?.[index]||'engaged';
  return {
    pace:production.voicePace??1,
    emotion,
    intensity:scene.emotionalPlan?.intensities?.[index]??.5,
    delivery:scene.emotionalPlan?.voiceDirections?.[index]||`Clear, natural narration with ${emotion} and purposeful emphasis; avoid a flat or promotional cadence.`
  };
}
export function narrationInputHash(direction,production){
  const engine=production.voiceEngine||'piper';
  const voiceId=production.voiceId||(engine==='qwen'?'Ryan':'en_US-ljspeech-medium');
  return createHash('sha256').update(JSON.stringify({engine,voiceId,direction})).digest('hex');
}
