===================================
How to create a plugin for yeahyeah
===================================

<TODO: expand this into an actual tutorial. For now just pointers>


* Create a new package `yourplugin_plugin`
* Inside, create a module `cli.py`
* In cli.py, use the following structure::

        @click.group(name='yourplugin')
        @click.pass_context
        def main(ctx):
            """Yourplugin description"""
            #ctx




