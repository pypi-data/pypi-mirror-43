=====
jptel
=====

jptel は日本の電話番号を市外局番・市内局番・加入者番号に分割して返します。

This package is utility for japaneses telephone number.


インストール
+++++++++++++

::

  $ pip install jptel


使い方
++++++

.. code-block:: python

  >>> import jptel
  >>> jptel.normalize('0123456789')
  '0123-45-6789'
  >>> jptel.normalize('０１２３４５６７８９')
  '0123-45-6789'

  >>> jptel.validate('0123456789')
  True
  >>> jptel.validate('022252-2222')
  False

  >>> jptel.split('0312345678')
  {'area_code': '03', 'city_code': '1234',   'subscriber_code': '5678'}
  >>> jptel.split('00000000000')
  exception.InvalidTelephoneNumberException


その他
+++++++
固定電話の市外局番データは総務省のサイトからダウンロードできるExcelから生成しています。 再生成する場合は以下の手順で行って下さい。

::

  $ pip install -r dev_requirements.txt
  $ python _generate_master_data.py
