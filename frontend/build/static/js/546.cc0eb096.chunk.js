(self.webpackChunkfrontend = self.webpackChunkfrontend || []).push([
  [546],
  {
    6546: (e, s, c) => {
      c.r(s), c.d(s, { default: () => t });
      var r = c(2483),
        a = c(4666),
        i = c(149),
        n = c(5250),
        l = c(8964),
        d = c(8940),
        o = c(6723);
      const t = () => {
        const { token: e } = (0, a.g)(),
          { status: s, message: c, errors: t, data: u } = (0, l.M7)();
        return (
          (0, r.useEffect)(() => {
            "succeeded" === s
              ? (0, d.aT)("success", c)
              : "failed" === s && (0, d.aT)("error", c);
          }, [c, s]),
          (0, i.RT)(() => {
            (0, l.rn)();
          }),
          (0, o.jsxs)("div", {
            className: "verify-user-account-page",
            children: [
              (0, o.jsxs)("div", {
                className: "header",
                children: [
                  (0, o.jsx)("h3", {
                    className: "form-label",
                    children: "Verify your account",
                  }),
                  (0, o.jsx)("p", {
                    className: "form-description",
                    children:
                      "Click the Verify button below to verify your account.",
                  }),
                ],
              }),
              (0, o.jsxs)("form", {
                className: "form",
                onSubmit: (s) => {
                  s.preventDefault(), (0, l.MO)({ token: e || "" });
                },
                children: [
                  (0, o.jsx)(n.q_, { field: "none", errors: t }),
                  (0, o.jsx)(n.q_, { field: "token", errors: t }),
                  (null === u || void 0 === u ? void 0 : u.detail) &&
                    (0, o.jsx)("p", { children: u.detail }),
                  (0, o.jsxs)("div", {
                    className: "actions",
                    children: [
                      (0, o.jsx)(n.k2, {
                        to: "../../",
                        type: "link",
                        className: "link back-link",
                        iconName: "arrowBack",
                        children: "Back",
                      }),
                      (0, o.jsx)(n.$n, {
                        type: "submit",
                        iconName: "succeeded" === s ? "checkCircle" : "click",
                        className: "button",
                        isLoaderOn: "loading" === s,
                        isDisabled: "succeeded" === s,
                        children: "Verify",
                      }),
                    ],
                  }),
                  "succeeded" === s && (0, o.jsx)(n.xP, {}),
                ],
              }),
            ],
          })
        );
      };
    },
  },
]);
//# sourceMappingURL=546.cc0eb096.chunk.js.map
