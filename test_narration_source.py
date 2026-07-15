from copy import deepcopy
from engine.game_engine import GameEngine
from engine.narration_prompt import build_narration_prompt_packet
from engine.narration_request import build_narration_request_packet
from engine.narration_source import NARRATION_SOURCE_METADATA, build_openai_responses_narration_source_result, validate_narration_source_result_packet
import os

def main():
    prompt = build_narration_prompt_packet(build_narration_request_packet(GameEngine('data/regions/bryn_shander.json').get_narration_context('look around')))
    old=os.environ.get('OPENAI_API_KEY'); os.environ['OPENAI_API_KEY']='test'
    class Response: status='completed'; output_text='A hard wind crosses the gate.'
    result=build_openai_responses_narration_source_result(prompt, lambda client, request: Response())
    assert result['metadata']==NARRATION_SOURCE_METADATA
    assert validate_narration_source_result_packet(result,prompt)==result
    bad=deepcopy(result); bad['metadata']['model']='other'
    try: validate_narration_source_result_packet(bad,prompt); raise AssertionError('metadata accepted')
    except ValueError: pass
    if old is None: os.environ.pop('OPENAI_API_KEY',None)
    else: os.environ['OPENAI_API_KEY']=old
    print('Narration source test passed.')
if __name__ == '__main__': main()
