# How to add services

For now, there isn't a graphical/nice way to add services to the manager.  You
will have to edit the file `src/services.json` to add more.

The syntax follows the [JSON standard][json-standard].

There are two parts to the file:
* a categories list
* a list of services

The categories list is at the top, under the `Categories` tag.

The services list is below that, under the `services` tag.

Each category should be a string, and no more.

For each service, the following must be provided as strings:

| Field           | Description                                             |
| --------------- | ------------------------------------------------------- |
| `name`          | A user-friendly name for the service                    |
| `computer_name` | The process name                                        |
| `category`      | What category the services falls under (case-sensitive) |
| `start`         | Bash command for starting the service                   |
| `stop`          | Bash command for stopping the service                   |

For example:

```json
{
  "name": "Nessus",
  "computer_name": "nessusd",
  "category": "Security",
  "start": "/etc/init.d/nessusd start",
  "stop": "/etc/init.d/nessusd stop"
}
```

When you're done editing, simply save the file and re-run the program.


[json-standard]: www.w3schools.com/js/js_json_syntax.asp