"""Limited owner smoke: explicit fixtures, common GameEngine runtime, offline.

Run from repository root with the official interpreter: -m tools.smoke_i2.
This is a test supplier surface, not production language or domain coverage.
"""
import argparse
from engine.consequence_integration import FactEffect
from engine.information_resolution import Identity
from test_fixtures.consequence_suppliers import Premises, engine, request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', action='store_true', help='Supply a hidden binding condition')
    parser.add_argument('--exception', action='store_true', help='Supply its legitimate exception')
    parser.add_argument('--scripted', action='store_true', help='Run the finite offline smoke sequence')
    args = parser.parse_args()
    premises = Premises()
    if args.binding:
        premises.ward()
    if args.exception:
        premises.change('permit', 'yes')
    e = engine(premises, effects=(FactEffect('lift', 'gap', 'usable', 'yes',
        identity=Identity('gap'), relation_from='target', relation='governs', visible=True),))
    print('Fixture: a manageable obstruction, one expendable wedge, supported lifting competence.')
    print('I2 continuity lasts only in this engine. Save/load is unavailable.')
    print('Commands: attempt, retry, use opening, save, quit.')
    scripted = iter(('attempt', 'retry', 'use opening', 'save', 'quit')) if args.scripted else None
    while True:
        command = next(scripted) if scripted else input('> ').strip().lower()
        if scripted:
            print('> ' + command)
        if command == 'quit':
            break
        if command == 'save':
            try:
                e.save('.artifacts/i2-smoke-must-not-write.json')
            except ValueError as error:
                print(str(error))
            else:
                raise AssertionError('I2 must refuse incomplete saves')
            continue
        if command in {'attempt', 'retry'}:
            result = e.process_consequence(request('smoke-attempt'))
        elif command == 'use opening':
            result = e.process_consequence(request('smoke-use', target='gap', method='use', means=()))
        else:
            print('Choose a supported fixture command.')
            continue
        print(result['message'])
        # Owner-visible runtime evidence, never a player-facing hidden premise dump.
        state = e.get_consequence_state().adjudication
        print(f'Accepted time: {state.at}; wedges: {state.inventory[0][2]}.')


if __name__ == '__main__':
    main()
