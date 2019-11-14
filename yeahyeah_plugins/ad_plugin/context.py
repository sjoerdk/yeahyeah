"""Context that gets passed around to this yeahyeah_plugins' functions

"""
import click
from umcnad.core import ADConnection


class ADPluginContext:
    """Context that gets passed to each ad_plugins function

    """
    def __init__(self, server_url, bind_dn):
        self.server_url = server_url
        self.bind_dn = bind_dn

    def search_people(self, search_string):
        with ADConnection(url=self.server_url, bind_dn=self.bind_dn,
                          password=click.prompt('password for umcn AD')) as connection:
            return connection.search_people(search_string)

    @classmethod
    def init_from_dict(cls, dict_in):
        return cls(server_url=dict_in["server_url"], bind_dn=dict_in["bind_dn"])

    def to_dict(self):
        return {"server_url": self.server_url, "bind_dn": self.bind_dn}


pass_ad_context = click.make_pass_decorator(ADPluginContext)
default_context = ADPluginContext(
    server_url="<ldap://adserver:port>",
    bind_dn="<ldap dn to access AD. Something looking like 'cn=bla,ou=blab,dc=thing'>"
)
default_settings_file_name = "ad_umcn.json"