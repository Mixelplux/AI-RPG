"""All 15 package acceptance groups, offline through the public engine/CLI seam."""
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
from io import StringIO
import json
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch

NETWORK_ATTEMPTS = []
def no_network(*args, **kwargs):
    NETWORK_ATTEMPTS.append(True)
    raise AssertionError("Network/provider forbidden")
socket.socket.connect = no_network
socket.socket.connect_ex = no_network
socket.create_connection = no_network

import play_game
from engine.game_engine import GameEngine
from engine import game_engine as engine_module
from engine import west_road_predicament as west
from engine import character_competence as competence
from engine.contextual_investigation import ActionFrame, Candidate, interpret
from engine.save_system import build_save_data, load_game
from engine.north_gate_discussion import NorthGateDiscussion
from engine.scene_composition import prepare_scene_revised_a

REGION = 'data/regions/bryn_shander.json'
DEPOT = 'test_fixtures/contextual_investigation_depot.json'
EVIDENCE = Path(r'C:\tmp\AI-RPG-Contextual-Investigation-V1-Implementation')
TRACKS = 'Examine those off-road marks for signs that people watched the wagons.'
SURVEY = "Look for useful leads near the road; don't question anyone or follow a trail."
REPORT = "Tell Elin what the tracks suggest, but don't mention Mara's account."

class DepotPolicy:
    """Independent concrete access policy; not a production region or registry."""
    def candidates(self, engine):
        local = engine.get_world_state()['player']['current_location_id']
        declarations = {d['discovery_id']: d for d in engine.region['discovery_declarations']}
        result = []
        for identity, label, cue, aliases, purposes in (
            ('seal', 'crate seal', 'A crate seal is available to inspect.', ('seal', 'crate seal'), ('seal', 'opened')),
            ('tally', 'chalk tally', 'A chalk tally is available to read.', ('tally', 'chalk tally'), ('deliveries', 'recorded', 'count'))):
            decl = declarations[identity]
            expected = {'trace_id': decl['trace_id'], 'evidence_id': identity, 'location_id': local}
            if local == 'depot' and engine.get_evidence_trace(decl['trace_id']) == expected:
                result.append(Candidate(decl['trace_id'], 'evidence', label, cue, aliases, purposes, identity))
        return tuple(result)
    def findings(self, engine):
        return tuple(Candidate(d['discovery_id'], 'finding', d['title'], d['text'], (d['title'].casefold(),), (), d['discovery_id'])
            for d in engine.region['discovery_declarations'] if d['discovery_id'] in engine.get_player_discoveries())
    def recipients(self, engine):
        return ()
    def ask(self, engine, candidate):
        return None


def road():
    return GameEngine(REGION, entry_location_id=west.ROAD)

def depot():
    e = GameEngine(DEPOT, investigation_policy=DepotPolicy())
    for d in e.region['discovery_declarations']:
        e.create_evidence_trace(d['trace_id'], d['discovery_id'], d['location_id'])
    return e

def ready():
    e = road()
    e.process_command('investigate')
    e.process_command('talk to Mara')
    e.process_command('go to North Gate')
    return e

def cli(e, commands, **adapters):
    output = StringIO()
    with patch.object(play_game.GameEngine, 'start_new', return_value=e), \
         patch('builtins.input', side_effect=list(commands) + ['quit']), redirect_stdout(output):
        play_game.main(**adapters)
    return output.getvalue()

class Acceptance(unittest.TestCase):
    def setUp(self):
        self.provider = patch('engine.narration_source.OpenAI', side_effect=no_network)
        self.provider.start()
        self.addCleanup(self.provider.stop)
        EVIDENCE.mkdir(parents=True, exist_ok=True)

    def unchanged(self, e, before):
        self.assertEqual(e.get_world_state(), before)

    def test_01_arrival_survey_rendering_purity(self):
        e = road(); before = e.get_world_state(); save = build_save_data(e)
        for _ in range(2):
            e.get_player_perception(); e.get_current_scene_projection(); e.get_narration(); e.get_scene_narration()
            r = e.process_command('Survey the area for leads')
            self.assertEqual(r['contextual']['status'], 'survey')
            self.assertNotIn("Mara reports", r['message'])
            self.assertNotIn('deliberate observation', r['message'])
        self.unchanged(e, before); self.assertEqual(build_save_data(e), save)
        self.assertEqual(e.get_player_discoveries(), ())
        gate = GameEngine(REGION)
        self.assertEqual(gate.get_investigation_context()['leads'], [])

    def test_02_scope_constraints_and_stop(self):
        for command in (SURVEY, 'Search for ground signs; stay nearby and stop after the first useful lead',
                        'Look for clues without questioning anyone',
                        "Look for clues and don't question anyone"):
            e = road(); before = e.get_world_state(); r = e.process_command(command)
            self.assertEqual(r['contextual']['status'], 'survey', command)
            self.assertNotIn('Mara', r['message'])
            self.unchanged(e, before)
        e = road(); before = e.get_world_state()
        for command in ('Examine marks and ask Mara what she saw', 'Examine marks, then follow the trail',
                        "Examine marks; don't touch anything", 'Survey the area; stop when a guard arrives', 'Examine marks; stop after a reply',
                        "Tell Elin about the tracks and Mara's account", 'Examine marks and conceal them',
                        'Examine marks using magic', "Examine marks; don't follow the trail and question Mara"):
            self.assertFalse(e.process_command(command)['success'], command)
            self.unchanged(e, before)

    def test_03_direct_purpose_and_order_selection(self):
        for reverse in (False, True):
            e = road()
            if reverse: e.region['discovery_declarations'].reverse()
            r = e.process_command(TRACKS)
            self.assertTrue(r['success']); self.assertEqual(e.get_player_discoveries(), ('west_road_tracks',))
            self.assertEqual(r['contextual']['frame']['operation'], 'examine')
        e = depot(); e.region['discovery_declarations'].reverse()
        r = e.process_command('Check what deliveries are recorded')
        self.assertTrue(r['success']); self.assertEqual(e.get_player_discoveries(), ('tally',))
        e = depot(); self.assertTrue(e.process_command('Inspect the crate seal')['success'])
        self.assertEqual(e.get_player_discoveries(), ('seal',))

    def test_04_qualified_findings_and_access(self):
        e = road(); r = e.process_command(TRACKS)
        self.assertIn('suggest', r['message']); self.assertIn('not identity or an attack', r['message'])
        e = road(); before=e.get_world_state()
        e.world_state['evidence_traces'] = []
        removed = e.get_world_state()
        self.assertFalse(e.process_command(TRACKS)['success']); self.unchanged(e, removed)
        gate = GameEngine(REGION); before=gate.get_world_state()
        self.assertFalse(gate.process_command(TRACKS)['success']); self.unchanged(gate, before)
        d=depot(); self.assertEqual(len(d.get_investigation_context()['leads']), 2)
        self.assertNotIn('Annex', json.dumps(d.get_investigation_context()['leads']))

    def test_05_separate_mara_and_duplicate(self):
        e=road(); before=e.get_world_state()
        self.assertFalse(e.process_command('Ask Mara where the hidden camp is')['success'])
        self.unchanged(e,before)
        r=e.process_command('Ask Mara what she actually saw')
        self.assertIn('Mara reports',r['message']); self.assertEqual(e.get_player_discoveries(), ('west_road_merchant_account',))
        self.assertEqual(e.get_actor_knowledge(west.ELIN), ())
        accepted=e.get_world_state(); self.assertTrue(e.process_command('Ask Mara what she actually saw')['success'])
        self.unchanged(e,accepted)
        g=GameEngine(REGION); before=g.get_world_state()
        self.assertFalse(g.process_command('Ask Mara what she actually saw')['success']); self.unchanged(g,before)

    def test_06_selective_receipt_and_no_broadcast(self):
        e=ready(); before=e.get_world_state()
        self.assertEqual(e.get_actor_knowledge(west.ELIN), ())
        self.assertTrue(e.process_command(REPORT)['success'])
        self.assertEqual(e.get_actor_knowledge(west.ELIN), (west.shared_id('west_road_tracks'),))
        self.assertEqual(e.get_actor_knowledge(west.GREY), ())
        accepted=e.get_world_state(); self.assertTrue(e.process_command(REPORT)['success']); self.unchanged(e,accepted)
        g=GameEngine(REGION); before=g.get_world_state()
        self.assertFalse(g.process_command(REPORT)['success']); self.unchanged(g,before)
        e=ready(); before=e.get_world_state()
        self.assertFalse(e.process_command('Tell Elin about the tracks and Mara account')['success']); self.unchanged(e,before)
        e=ready(); self.assertTrue(e.process_command('Share the tracks with Elin')['success'])
        self.assertEqual(e.get_actor_knowledge(west.ELIN),(west.shared_id('west_road_tracks'),))

    def test_07_existing_decision_prerequisites(self):
        e=ready(); e.process_command(REPORT)
        self.assertFalse(e.process_command('advocate patrol')['success'])
        self.assertTrue(e.process_command("Tell Elin Mara's account too")['success'])
        self.assertEqual(set(west.available_commands(e.get_world_state(),e.get_scene_snapshot())), {'advocate patrol','continue investigation'})
        discussion=NorthGateDiscussion(); discussion.control(e,'discuss patrol with Elin')
        before=e.get_world_state(); self.assertTrue(e.process_command('resume investigation')['success'])
        self.unchanged(e,before)
        self.assertEqual(e._investigation_focus.snapshot()['status'],'active')
        self.assertTrue(e.process_command('advocate patrol')['success'])
        self.assertEqual(e.get_world_state()['time']['elapsed_hours'], before['time'].get('elapsed_hours',0)+1)
        self.assertIsNone(e._investigation_focus.snapshot())

    def test_08_raw_and_structured_frames(self):
        e=road(); frame=interpret('Examine the marks without following anyone',e)
        self.assertIsInstance(frame,ActionFrame); self.assertIn('no_following',frame.constraints)
        self.assertEqual(frame.method,'inspect_evidence'); self.assertEqual(frame.stop_boundary,'finding')
        self.assertTrue(e.process_contextual_investigation(frame=frame)['success'])
        d=depot(); before=d.get_world_state()
        self.assertFalse(d.process_command('Examine the evidence')['success']); self.unchanged(d,before)
        for bad in (replace(frame,operation=[]), replace(frame,method='climb'), replace(frame,stop_boundary='capture'), replace(frame,constraints=('new_power',)), replace(frame,constraints=(7,)), replace(frame,constraints=('exclude:west_road_tracks',)), replace(frame,constraints=('exclude:invented',))):
            before=e.get_world_state(); self.assertFalse(e.process_contextual_investigation(frame=bad)['success']); self.unchanged(e,before)
        e=road(); before=e.get_world_state()
        self.assertFalse(e.process_command("Ask Mara what she saw, but don't question her")['success']); self.unchanged(e,before)

    def test_09_focus_lifecycle_and_revalidation(self):
        e=road(); e.process_command(TRACKS); focus=e._investigation_focus.snapshot()
        e.process_command('go to North Gate'); self.assertEqual(e._investigation_focus.snapshot()['status'],'suspended')
        e.process_command('go to Southwest Trade Road'); self.assertEqual(e._investigation_focus.snapshot()['status'],'suspended')
        before=e.get_world_state(); self.assertTrue(e.process_command('Examine those marks')['success']); self.unchanged(e,before)
        e.process_command('cancel investigation'); self.assertIsNone(e._investigation_focus.snapshot()); self.unchanged(e,before)
        e.process_command('Survey for leads'); focus=e._investigation_focus.snapshot()
        before=e.get_world_state()
        for confirmation in ('yes','continue','yes, continue'):
            self.assertFalse(e.process_command(confirmation)['success']); self.unchanged(e,before)
        with patch('engine.game_session.GameSession.reset',side_effect=ValueError('supplied invalid reset')):
            with self.assertRaises(ValueError): e.reset()
        self.unchanged(e,before); self.assertEqual(e._investigation_focus.snapshot(),focus)
        with patch('engine.save_system.load_game',side_effect=ValueError('supplied invalid load')):
            with self.assertRaises(ValueError): e.load(str(EVIDENCE/'missing.json'))
        self.assertEqual(e._investigation_focus.snapshot(),focus)
        path=EVIDENCE/'group09_save.json'; e.save(str(path)); self.assertEqual(e._investigation_focus.snapshot(),focus)
        e.load(str(path)); self.assertIsNone(e._investigation_focus.snapshot())
        before=e.get_world_state(); self.assertFalse(e.process_command('Examine that')['success']); self.unchanged(e,before)
        e.process_command('Survey for leads'); e.reset(); self.assertIsNone(e._investigation_focus.snapshot())
        for control in ('load','reset'):
            e=road(); e.save(str(path))
            with patch.object(play_game,'SAVE_PATH',str(path)):
                out=cli(e,['Survey for leads',control])
            self.assertIn('investigation focus ends on '+control,out)
        e=road()
        with patch.object(play_game,'SAVE_PATH',str(EVIDENCE/'absent_owner_smoke_save.json')):
            out=cli(e,['Survey for leads','load'])
        self.assertNotIn('investigation focus ends on load',out)
        d=depot(); d.process_command('Inspect crate seal'); d.world_state['evidence_traces']=[t for t in d.world_state['evidence_traces'] if t['trace_id']!='seal_trace']
        before=d.get_world_state(); self.assertFalse(d.process_command('Examine that')['success']); self.unchanged(d,before)

    def test_10_exact_selected_replay(self):
        e=depot(); e.process_command('Inspect crate seal'); before=e.get_world_state()
        for action in ('Inspect crate seal','Examine that'):
            r=e.process_command(action); self.assertEqual(r['contextual']['status'],'already_acquired'); self.unchanged(e,before)
        self.assertEqual(e.get_player_discoveries(),('seal',))
        e=road(); e.process_command(TRACKS); before=e.get_world_state()
        e.process_command('Ask Mara what she saw'); acquired=e.get_world_state()
        e.process_command('finish investigation'); self.unchanged(e,acquired)
        self.assertIn('west_road_tracks',e.get_player_discoveries())

    def test_11_atomic_failure_boundaries(self):
        for failure in ('add_history_entry','validate_world_state','build_scene'):
            e=road(); e.process_command('Survey for leads'); before=e.get_world_state(); scene=e.get_scene_snapshot(); focus=e._investigation_focus.snapshot()
            with patch.object(engine_module,failure,side_effect=ValueError('supplied '+failure)):
                with self.assertRaises(ValueError): e.process_command(TRACKS)
            self.unchanged(e,before); self.assertEqual(e.get_scene_snapshot(),scene); self.assertEqual(e._investigation_focus.snapshot(),focus)
            e=ready(); e.process_command('Survey for leads'); before=e.get_world_state(); scene=e.get_scene_snapshot(); focus=e._investigation_focus.snapshot()
            with patch.object(engine_module,failure,side_effect=ValueError('supplied '+failure)):
                with self.assertRaises(ValueError): e.process_command(REPORT)
            self.unchanged(e,before); self.assertEqual(e.get_scene_snapshot(),scene); self.assertEqual(e._investigation_focus.snapshot(),focus)

    def test_12_save_version_and_shape_compatibility(self):
        e=road(); initial=build_save_data(e); e.process_command(SURVEY)
        self.assertEqual(initial,build_save_data(e))
        states=[e.get_world_state()]
        e.process_command(TRACKS); states.append(e.get_world_state())
        e.process_command('Ask Mara what she saw'); e.process_command('go to North Gate'); e.process_command(REPORT); states.append(e.get_world_state())
        e.process_command("Tell Elin Mara's account too"); e.process_command('continue investigation'); states.append(e.get_world_state())
        for index,state in enumerate(states):
            clone=GameEngine(REGION,initial_world_state=state); path=EVIDENCE/f'group12_{index}.json'; clone.save(str(path))
            restored=load_game(str(path)); self.assertEqual(build_save_data(restored),build_save_data(clone))
            self.assertEqual(set(build_save_data(restored)),{'save_version','region_path','world_state'})
            self.assertEqual(build_save_data(restored)['save_version'],1); self.assertEqual(set(state),set(initial['world_state']))
            self.assertNotIn('investigation_focus',json.dumps(build_save_data(restored)))
        malformed=deepcopy(initial); malformed['world_state'].pop('west_road_predicament')
        path=EVIDENCE/'group12_bad.json'; path.write_text(json.dumps(malformed)); before=e.get_world_state()
        with self.assertRaises(ValueError): e.load(str(path))
        self.unchanged(e,before)

    def test_13_independent_depot_access_and_staleness(self):
        d=depot(); before=d.get_world_state(); d.process_command('Survey for useful leads'); self.unchanged(d,before)
        self.assertEqual(len(d.get_investigation_context()['leads']),2)
        self.assertFalse(d.process_command('Inspect the annex note')['success']); self.unchanged(d,before)
        d.process_command('Inspect crate seal'); self.assertEqual(d.get_player_discoveries(),('seal',))
        before=d.get_world_state(); self.assertFalse(d.process_command('Tell the porter about the seal')['success']); self.unchanged(d,before)
        path=EVIDENCE/'group13_save.json'; d.save(str(path)); d.load(str(path)); self.assertIsNone(d._investigation_focus.snapshot())
        self.assertEqual(d.get_player_discoveries(),('seal',)); self.assertEqual(len(d.get_investigation_context()['leads']),2)
        self.assertNotIn('west_road',json.dumps(d.get_world_state()))
        # Identity, not similar labels or the next declaration, controls revalidation.
        d=depot(); d.process_command('Inspect crate seal'); d.world_state['evidence_traces']=[t for t in d.world_state['evidence_traces'] if t['trace_id']!='seal_trace']
        d.create_evidence_trace('similar_seal','seal','depot'); before=d.get_world_state()
        self.assertFalse(d.process_command('Examine that')['success']); self.unchanged(d,before)

    def test_14_projection_isolation_and_fallback(self):
        e=road(); before=e.get_world_state(); packet=e.get_investigation_context()
        packet['leads'][0]['ref']='forged'; packet['findings'].append({'ref':'invented'})
        self.unchanged(e,before); self.assertEqual(e.get_player_discoveries(),())
        sources=[]
        def prepare(source):
            sources.append(deepcopy(source)); source['selected_facts'].clear(); raise ValueError('adapter failure')
        e.process_command(TRACKS); accepted=e.get_world_state()
        result=e.get_scene_narration(preparer=prepare)
        self.assertFalse(result['accepted']); self.unchanged(e,accepted)
        self.assertTrue(sources)
        self.assertNotIn('west_road_tracks_trace',json.dumps(sources))
        with patch.object(e,'get_resolved_narration',side_effect=AssertionError('ordinary result misrouted')):
            output=cli(e,['Survey for leads',TRACKS,'go to North Gate',REPORT],scene_preparer=prepare)
        self.assertIn('suggest deliberate observation',output)
        self.assertNotIn('west_road_tracks_trace',output)

    def test_15_cli_and_existing_competence(self):
        e=road(); output=cli(e,[SURVEY,TRACKS,'Ask Mara what she actually saw','go to North Gate',REPORT,"Tell Elin Mara's account too",'advocate patrol'])
        self.assertIn('Marks away from the wagon path',output)
        self.assertEqual(e.get_actor_knowledge(west.ELIN),tuple(west.shared_id(d) for d in west.INITIAL_EVIDENCE))
        self.assertEqual(e.get_world_state()['west_road_predicament']['phase'],'observers_withdrew')
        self.assertIn('local investigation focus is suspended',output)
        for operation in competence.OPERATIONS:
            e=ready(); e.present_clue("Repeated Watch Tracks","Elin"); e.present_clue("Mara's Account","Elin"); e.process_command('advocate patrol')
            with patch.object(competence,'draw_d6',return_value=1):
                r=e.process_command(operation)
            self.assertEqual(r['intent'],'west_road_competence',operation)
            accepted=e.get_world_state(); e.process_command(operation); self.unchanged(e,accepted)
        self.assertEqual(NETWORK_ATTEMPTS,[])

if __name__ == '__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Acceptance)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'groups_run':result.testsRun,'failed':len(result.failures),'errors':len(result.errors),
            'network_attempts':len(NETWORK_ATTEMPTS),'passed':result.wasSuccessful(),
            'failures':[name.id() for name,_ in result.failures+result.errors]}
    (EVIDENCE/'acceptance_results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)