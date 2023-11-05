.. used to do a basic sanity test on the data template extension

Data Template Test
=====================

See `<https://sphinxcontribdatatemplates.readthedocs.io/en/latest/inline.html>`_

.. datatemplate:json:: sample.json

   Individual Item
   ~~~~~~~~~~~~~~~

   {{ data['key1'] }}

   List of Items
   ~~~~~~~~~~~~~

   {% for item in data['key2'] %}
   - {{item}}
   {% endfor %}

   HTML Context
   ~~~~~~~~~~~~

   {% for key, value in config.html_context.items() %}
   - ``{{key}}`` = ``{{value}}``
   {% endfor %}