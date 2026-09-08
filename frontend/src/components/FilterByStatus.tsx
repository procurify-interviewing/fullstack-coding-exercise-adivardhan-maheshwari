import * as React from "react";

export const FilterByStatus = () => {
  return (
    <div>
      <label htmlFor="status-filter">status filter</label>
      <select
        id="status-filter"
        // value={}
        // onChange={}
      >
        <option value="all">All</option>
      </select>
    </div>
  );
};
