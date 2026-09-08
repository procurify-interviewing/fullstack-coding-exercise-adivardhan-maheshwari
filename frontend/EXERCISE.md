# Frontend: View purchase requests

Build a REACT component that shows purchase requests requiring my approval.

## Part 1: fetch and render a list of purchase requests

- Call this endpoint: `GET: /api/purchase-requests`, as implemented in the backend coding exercise.
  - use react hooks to fetch the list of purchase requests and store them in `<App />` state on component mount
- Pass the list of PRs returned by the GET request to `<ListRequests />`
  - define component props
  - render a table with a static header row and dynamic content rows
    - Amount
    - Requester Name
    - Status

## Part 2: Introduce pagination

- Modify API Fetch:
  - Update the data fetching logic to accept and send `limit` and `offset` parameters to the API, simulating data fetching in chunks.
- Implement "Load More":
  - Add a button at the bottom of the list that fetches the next page of results and appends them to the existing list, rather than replacing the list

## If time permits:

### Filter by status

- In `App.tsx`, render `<FilterByStatus />` under `<ListRequests />`
- Update `FilterByStatus.tsx` to render dropdown options for each possible purchase request status, as well as ALL
- On select, filter the list of requests shown by that status
  - when ALL is selected, show all purchase requests

### Additional nice to have's

- Loading state
- Basic error handling
- Styling
- Unit tests

## PROJECT STRUCTURE

- `/src/App.tsx`: the file housing your root component.
- `/src/components/` the folder housing your helper components.
- `/src/tests/App.spec.tsx`: optional test file you can flesh out if time permits.
- `/package.json`: if you choose to add new dependencies.
