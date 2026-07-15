from engine.game_engine import GameEngine
from engine.narration_pipeline import build_narration_preview_packet
from engine.narration_source import NARRATION_SOURCE_METADATA

def main():
    engine=GameEngine('data/regions/bryn_shander.json'); context=engine.get_narration_context('look around'); before=engine.get_world_state()
    def fake(prompt): return {'schema':'ai_rpg.narration_source_result','version':1,'source':'openai_responses_preview','source_prompt':prompt,'candidate':{'schema':'ai_rpg.narration_output_packet','version':1,'narration_text':'Snow folds over the stones.'},'metadata':NARRATION_SOURCE_METADATA}
    packet=build_narration_preview_packet(context,source_builder=fake)
    assert packet['accepted'] and packet['source']=='openai_responses_preview' and packet['display_text']
    assert engine.get_world_state()==before
    print('Narration pipeline test passed.')
if __name__ == '__main__': main()
