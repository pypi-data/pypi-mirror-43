import requests

from mooshak2api.factory import GenericObject


class Evaluation(GenericObject):
    type = "evaluation_summary"

    def __init__(self, contest_id, problem_id, *args, **kwargs):
        super(Evaluation, self).__init__()
        self.contest_id = contest_id
        self.problem_id = problem_id

    def refresh(self, connection):
        """
        Refreshes the data from the server
        :param connection:
        :return:
        """
        r = requests.get(
            f"{connection.endpoint}data/contests/{self.contest_id}/submissions/{self.id}/evaluation-summary",
            headers=connection.headers_with_auth()
        )
        self.load_from_dict(r.json())


