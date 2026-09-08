import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./components/App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

/**
 *
 * Use the following to render the application
 * if `msw` is needed to complete the Frontend coding exercise
 *
 */
// async function startMocks() {
//   const { worker } = await import("./mocks/browser");
//   await worker.start({
//     serviceWorker: {
//       url: "/mockServiceWorker.js",
//     },
//   });
// }

// startMocks().then(() => {
//   const root = ReactDOM.createRoot(document.getElementById("root")!);
//   root.render(
//     <React.StrictMode>
//       <App />
//     </React.StrictMode>,
//   );
// });
