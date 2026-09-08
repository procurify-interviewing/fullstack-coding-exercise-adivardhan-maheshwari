import { rest } from "msw";

let prs = [
  {
    id: 1,
    status: "PENDING",
    total_amount: 1.0,
    requires_my_approval: true,
    requester_name: "bob",
  },
  {
    id: 2,
    status: "PENDING",
    total_amount: 1.01,
    requires_my_approval: true,
    requester_name: "bob",
  },
  {
    id: 3,
    status: "PENDING",
    total_amount: 1.02,
    requires_my_approval: true,
    requester_name: "alice",
  },
  {
    id: 4,
    status: "APPROVED",
    total_amount: 1.03,
    requires_my_approval: false,
    requester_name: "bob",
  },
  {
    id: 5,
    status: "REJECTED",
    total_amount: 1.04,
    requires_my_approval: false,
    requester_name: "alice",
  },
];

/**
 * Artificial response delay in ms, applied to GET.
 */
const GET_DELAY_MS = 400;

export const handlers = [
  /**
   * GET /api/purchase-requests/?status=&limit=&offset=
   *
   * status - filter by status.
   * limit  - page size. Omit to get the whole filtered list.
   * offset - where in the filtered list the page starts. Defaults to 0.
   *
   * Filtering runs before pagination.
   *
   * Responds 200 with an array of purchase requests.
   */
  rest.get("/api/purchase-requests/", (req, res, ctx) => {
    const status = req.url.searchParams.get("status");

    const limit = req.url.searchParams.has("limit")
      ? Number(req.url.searchParams.get("limit"))
      : null;
    const offset = Number(req.url.searchParams.get("offset")) || 0;

    const filtered = status ? prs.filter((pr) => pr.status === status) : prs;

    const page =
      limit === null ? filtered : filtered.slice(offset, offset + limit);

    return res(ctx.delay(GET_DELAY_MS), ctx.json(page));
  }),
];
