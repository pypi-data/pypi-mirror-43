import requests

from mooshak2api.factory import GenericObject


class Contest(GenericObject):
    """
    A Mooshak2 Contest. The only required property that is required is an ID
    """

    def update(self, connection):
        r = requests.put(
            f"{connection.endpoint}data/contests/{self.id}/",
            headers=connection.headers_with_auth(),
            json=self.as_json()
        )
        return r

    def delete(self, connection):
        r = requests.delete(
            f"{connection.endpoint}data/contests/{self.id}/",
            headers=connection.headers_with_auth()
        )
        return r

    def create(self, connection):
        r = requests.post(
            f"{connection.endpoint}data/contests/",
            headers=connection.headers_with_auth(),
            json=self.as_json()
        )
        return r


def get(connection, contest_id):
    r = requests.get(f"{connection.endpoint}data/contests/{contest_id}/", headers=connection.headers_with_auth())
    return Contest().load_from_dict(r.json())


def all(connection):
    r = requests.get(f"{connection.endpoint}data/contests/", headers=connection.headers_with_auth())
    results = []
    for c in r.json():
        results.append(Contest().load_from_dict(c))
    return results

