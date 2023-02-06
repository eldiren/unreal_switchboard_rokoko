Unreal Switchboard Rokoko Device
===========================

Unreal Switchboard Rokoko Device is a python plugin for Unreal Switchboard.

Supported Platforms
-------------------

Works on all support Unreal Engine platforms

Dependencies
------------

Switchboard dependencies, and default python libs only.

Building and running
------------

Plugin gets installed to
<Unreal Engine Folder>\Engine\Plugins\VirtualProduction\Switchboard\Source\Switchboard\switchboard\devices

You add the device to switchboard and specify the Rokoko Command API port and IP address Rokoko Studio is running on. Switchboard doesn't have any way we know of to raise errors so check exceptions in try/except blocks.

Testing
-------------

Something like REST Client in VSCode will allow you to sanity check the Command API connection. Name a file rokoko.http and add these lines:

```
POST http://127.0.0.1:14053/v1/1234/recording/start

###

POST http://127.0.0.1:14053/v1/1234/recording/stop
```

You can then test startign and stopping record to verify connectivity.