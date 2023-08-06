# How to use
The application depends on a running Postgres and Redis configuration.  

### Worker Setup
#### 1. Creating a worker
There are 2 important things when you create your own worker:

1. **Package the module on the correct namespace**
We're using the namespace declared in the `setup.py` file as an entrypoint to be able to recognize new workers.  
If workers do not follow this declaration, they won't be detectable by the schedulers and invisible to the system.  
```eval_rst
.. image:: images/setup_example.png
```

More information regarding entrypoints in packaging, can be found [here](https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata).

2. **Adhere to the correct API**
Every worker shall be called by importing the module and then calling `.start(context)` on it.  
The context is a dictionary containing specific required options.

In your `__init__.py`:

     def start(context):
         print("Hello, {}".format(context.get("name")))

3. **Publish worker on pip (or a private proxy)**
Make sure your worker is installable through pip on the location the schedulers will be running.
Install on the location of schedulers and synchronize the database by calling `python -m skidward publish_workers`.

If this is not available locally for a scheduler, it will update the task with the 'FAILED' status.

#### 2. Deploy and schedule
For workers to be run, we first need to have Schedulers running who pick up what needs to be done and spawn the processes.

1. **Run a scheduler**
```
$ python -m skidward start-scheduler
```
Optionally run it in the background as a process

    $ python -m skidward start-scheduler true

1. **Create the task**
This is done in the web interface, log in with admin credentials and create a new Task by selecting the appropriate worker and CRON string.
Because you can provide contexts to workers, 1 worker can have several functions based on the options you provide.
Every 5 seconds all schedulers wake up and check if there's a task to be executed.
If there is, a new process will be spawned and they will look for the next one.

- **Scheduled run**:
This is the default process; you create a task, provide it a worker, cron string and a context.
From here on out it will be run according to the schedule specified in the cron string.

- **Manual run**:
When viewing tasks, you can have a task execute as well at that time (outside of its schedule).
Go to a task and press 'run now'.

- **Configured run**:
When viewing tasks, you can have a manual task being run BUT with a changed configuration.
This is helpful when testing configurations or when you want to quickly run a change.
Go to a task and press 'configured run'.

