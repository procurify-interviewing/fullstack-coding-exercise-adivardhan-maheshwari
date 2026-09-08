# Backend: Purchase Requests API

Build an approver-aware Purchase Requests API that serves purchase requests over HTTP.

Make decisions on missing requirements, spend some time planning for the API implementation and read the question. Make sure you understand the values asked for in the responses and where it’s sourced from. You are free to change anything in the project in any way you like, but explain why. You are encouraged to talk through your decisions and contribute to the project as if this is going to be deployed in production.

## Part 1: List Purchase Requests
There are Purchase Requests that have been submitted by users for approval in the system. This API allows the current user to see their submitted requests along with requests that require the current user's approval.

`GET /api/purchase-requests/` returns the purchase requests the current user is allowed to
see:

- requests they created, or
- requests where they are an approver.


### Query parameters

The filter query parameters here are optional, and omitting them would return all records.

| Param | Values | Description |
| --- | --- | --- |
| `status` | `DRAFT`, `PENDING`, `APPROVED`, `REJECTED` | Filters by status |
| `requires_my_approval` | `true` | Only requests awaiting the current user's decision |


### Response

`GET /api/purchase-requests/?status=PENDING&requires_my_approval=true`

```json
// 200 OK
{
  "data": [
    {
      "id": 7,
      "requester_name": "alice",
      "status": "PENDING",
      "total_amount": "1000.00",
      "requires_my_approval": true
    }
  ]
}
```

- Each item contains `requires_my_approval` which is computed for the current user: `True` when the
user has an `Approval` row on the request whose `approved` is still null.
- Soft deleted records should not show up.

## Authentication

There is no auth layer in this project: `DEFAULT_AUTHENTICATION_CLASSES` is empty in
`config/settings.py`. Mock the current user however you like, and say which approach you
chose and why. The API is requested and treated as if it is requested by that user. 

Recommended to pick a seeded user (see [seed_data.py L79](src/purchase_requests/management/commands/seed_data.py)) so there is some data to see, such as Bob `id=2`.

### Demo and show it working

Walk through at least: an unfiltered result, a filtered result, and a request where the current
user can see results they do not need to approve.

Any one of these is fine:

- At root, `make run` or `make run-backend` and open
  <http://localhost:8000/api/purchase-requests/?status=PENDING&requires_my_approval=true>
  in a browser.
- Hit the same URL with `curl` or a local-accessible HTTP client if you have one
- Write an API test and run `make test-backend`. Fixtures
  live in `src/tests/conftest.py`, helpers in `src/tests/factories.py`.


## Part 2: Add pagination

Build pagination on the same API endpoint.

The API should now accept query parameters `limit` and `offset`, then return a `pagination` block alongside
`data`.


### Query parameters

| Param | Values | Description |
| --- | --- | --- |
| `limit` | integer | Page size, defaults to `10`. |
| `offset` | integer | Rows to skip, defaults to `0`. |
| `status`, `requires_my_approval` | | Continued from part 1 |

Some considerations:

- `limit` default and maximum
- ordering of records

### Response

`GET /api/purchase-requests/?limit=10&offset=10`

```json
// 200 OK
{
  "data": [
    {
      "id": 1,
      "requester_name": "carol",
      "status": "PENDING",
      "total_amount": "375.00",
      "requires_my_approval": false
    },
    ...
  ],
  "pagination": {
    "limit": 10,
    "offset": 10,
    "count": 21
  }
}
```

`count` is the total number of matching rows, not the size of the current page. This is used to help the frontend for knowing when the end of the results are.


### Show it working

Walk a couple of pages: `?limit=5&offset=0`,
`?limit=5&offset=5`, etc. Show that the ids neither repeat nor skip and the count reflects the complete list of filtered/unfiltered results.
