
import pyopenstates as pyos
import pandas as pd

pyopenstates_key = '2afed026-7ea2-422a-a4e7-95d740ee6be7'

class Chamber:

    pyos.set_api_key(pyopenstates_key)

    def __init__(self, state,chamber):
        self.state = state
        self.chamber= chamber
        self._members = None
        self._current_session_bills = None


    @property
    def members(self):
        if self._members is None:
             #df = pd.read_sql('',connection)


            print('...downloading.....')
            results=pyos.search_legislators(state=self.state,chamber=self.chamber)
            print('..parsing.......')
            df = pd.DataFrame(results)
            columns= ['id','all_ids','full_name','first_name','last_name','district','party','roles','created_at','updated_at']

            self._members = df[columns]
            #self._members['role_count'] = df['roles'].map(lambda x: len(x))

        return self._members

    @property
    def current_session_bills(self):
        if self._current_session_bills is None:

            print('...downloading.....')
            results=pyos.search_bills(state=self.state, chamber=self.chamber, search_window='session')
            print('..parsing.......')
            df = pd.DataFrame(results)
            columns= ['bill_id','title','action_dates', 'actions', 'created_at',
            'sources', 'sponsors', 'summary', 'updated_at', 'versions']

            if self.chamber =='upper':
                df = df[df.bill_id.str.startswith('S')]
                self._current_session_bills = df[columns]
            elif self.chamber == 'lower':
                df = df[df.bill_id.str.startswith('A')]
                self._current_session_bills = df[columns]
             #self._current_session_bills['sponsor_count'] = df['sponsors'].map(lambda x: len(x))

        return self._current_session_bills
