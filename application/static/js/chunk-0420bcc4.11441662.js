(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["chunk-0420bcc4"], {
    "42d8": function (e, t, n) {
    }, a5c9: function (e, t, n) {
    }, a9bc: function (e, t, n) {
        "use strict";
        n("a5c9")
    }, bb51: function (e, t, n) {
        "use strict";
        n.r(t);
        var a = n("7a23"), c = {class: "home"}, o = Object(a["h"])("hr", {class: "gap"}, null, -1),
            i = {key: 0, class: "tweet-wrapper"}, l = {class: "home__pagination"};

        function s(e, t, n, s, r, u) {
            var p = Object(a["C"])("add-tweet"), b = Object(a["C"])("tweet"), g = Object(a["C"])("v-pagination");
            return Object(a["u"])(), Object(a["g"])("div", c, [Object(a["k"])(p, {onSubmitClick: u.handleTweetSubmit}, null, 8, ["onSubmitClick"]), o, e.tweetData ? (Object(a["u"])(), Object(a["g"])("div", i, [(Object(a["u"])(!0), Object(a["g"])(a["a"], null, Object(a["A"])(e.tweetData, (function (e) {
                return Object(a["u"])(), Object(a["e"])(b, {
                    key: e.id,
                    "tweet-data": e,
                    onDeleteTweet: u.handleTweetDelete,
                    onGetTweets: u.getTweets
                }, null, 8, ["tweet-data", "onDeleteTweet", "onGetTweets"])
            })), 128))])) : Object(a["f"])("", !0), Object(a["h"])("div", l, [e.isPaginationEnabled ? (Object(a["u"])(), Object(a["e"])(g, {
                key: 0,
                modelValue: e.page,
                "onUpdate:modelValue": [t[0] || (t[0] = function (t) {
                    return e.page = t
                }), u.onPaginate],
                pages: Math.ceil(e.allTweetsCount / e.paginationLimit),
                "range-size": 1,
                "active-color": "#DCEDFF"
            }, null, 8, ["modelValue", "pages", "onUpdate:modelValue"])) : Object(a["f"])("", !0)])])
        }

        var r = n("1da1"), u = n("5530"), p = (n("96cf"), n("345e")), b = n("9257"), g = n("7424"), d = n("5502");
        const v = {viewBox: "0 0 8 2", fill: "none", xmlns: "http://www.w3.org/2000/svg"}, j = Object(a["k"])("path", {
            d: "M2.24 1c0 .556-.445 1-1 1-.556 0-1-.444-1-1s.444-1 1-1c.555 0 1 .444 1 1zm5.333 0c0 .556-.444 1-1 1-.555 0-1-.444-1-1s.445-1 1-1c.556 0 1 .444 1 1z",
            fill: "#BBB"
        }, null, -1);

        function O(e, t) {
            return Object(a["u"])(), Object(a["e"])("svg", v, [j])
        }

        var w = Object(a["l"])({
            name: "VPage",
            components: {IconPaginationDots: O},
            props: {
                page: {type: Number, default: null},
                current: {type: Number, default: 0},
                activeColor: {type: String, default: "#DCEDFF"}
            },
            emits: ["update"],
            setup(e, {emit: t}) {
                const n = Object(a["c"])(() => e.page === e.current);

                function c() {
                    t("update", e.page)
                }

                return {isActive: n, clickHandler: c}
            }
        });
        const h = Object(a["N"])("data-v-060ca318");
        Object(a["x"])("data-v-060ca318");
        const f = {key: 0, class: "DotsHolder"};
        Object(a["v"])();
        const m = h((e, t, n, c, o, i) => {
            const l = Object(a["C"])("icon-pagination-dots");
            return Object(a["u"])(), Object(a["e"])("li", null, [null === e.page ? (Object(a["u"])(), Object(a["e"])("span", f, [Object(a["k"])(l, {class: "Dots"})])) : (Object(a["u"])(), Object(a["e"])("button", {
                key: 1,
                class: ["Page", {"Page-active": e.isActive}],
                type: "button",
                "aria-label": "Go to page " + e.page,
                style: `background-color: ${e.isActive ? e.activeColor : "transparent"};`,
                onClick: t[1] || (t[1] = (...t) => e.clickHandler && e.clickHandler(...t))
            }, Object(a["F"])(e.page), 15, ["aria-label"]))])
        });
        w.render = m, w.__scopeId = "data-v-060ca318", w.__file = "src/components/atoms/VPage.vue";
        const C = {xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 24 24"},
            k = Object(a["k"])("path", {d: "M18.41 16.59L13.82 12l4.59-4.59L17 6l-6 6 6 6 1.41-1.41M6 6h2v12H6V6z"}, null, -1);

        function P(e, t) {
            return Object(a["u"])(), Object(a["e"])("svg", C, [k])
        }

        const x = {xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 24 24"},
            T = Object(a["k"])("path", {d: "M5.59 7.41L10.18 12l-4.59 4.59L7 18l6-6-6-6-1.41 1.41M16 6h2v12h-2V6z"}, null, -1);

        function V(e, t) {
            return Object(a["u"])(), Object(a["e"])("svg", x, [T])
        }

        const y = {xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 24 24"},
            D = Object(a["k"])("path", {d: "M15.41 16.58L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.42z"}, null, -1);

        function L(e, t) {
            return Object(a["u"])(), Object(a["e"])("svg", y, [D])
        }

        const B = {xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 24 24"},
            A = Object(a["k"])("path", {d: "M8.59 16.58L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.42z"}, null, -1);

        function F(e, t) {
            return Object(a["u"])(), Object(a["e"])("svg", B, [A])
        }

        var N = Object(a["l"])({
            name: "VPagination",
            components: {IconPageFirst: P, IconChevronLeft: L, IconChevronRight: F, IconPageLast: V, VPage: w},
            props: {
                pages: {type: Number, default: 0},
                rangeSize: {type: Number, default: 1},
                modelValue: {type: Number, default: 0},
                activeColor: {type: String, default: "#DCEDFF"},
                hideFirstButton: {type: Boolean, default: !1},
                hideLastButton: {type: Boolean, default: !1}
            },
            emits: ["update:modelValue"],
            setup(e, {emit: t}) {
                const n = Object(a["c"])(() => {
                    const t = [], n = 5 + 2 * e.rangeSize;
                    let a = e.pages <= n ? 1 : e.modelValue - e.rangeSize,
                        c = e.pages <= n ? e.pages : e.modelValue + e.rangeSize;
                    if (c = c > e.pages ? e.pages : c, a = a < 1 ? 1 : a, e.pages > n) {
                        const o = a - 1 < 3, i = e.pages - c < 3;
                        if (o) {
                            c = n - 2;
                            for (let e = 1; e < a; e++) t.push(e)
                        } else t.push(1), t.push(null);
                        if (i) {
                            a = e.pages - (n - 3);
                            for (let n = a; n <= e.pages; n++) t.push(n)
                        } else {
                            for (let e = a; e <= c; e++) t.push(e);
                            t.push(null), t.push(e.pages)
                        }
                    } else for (let e = a; e <= c; e++) t.push(e);
                    return t
                });

                function c(e) {
                    t("update:modelValue", e)
                }

                const o = Object(a["c"])(() => e.modelValue > 1), i = Object(a["c"])(() => e.modelValue < e.pages);

                function l() {
                    o.value && t("update:modelValue", 1)
                }

                function s() {
                    o.value && t("update:modelValue", e.modelValue - 1)
                }

                function r() {
                    i.value && t("update:modelValue", e.pages)
                }

                function u() {
                    i.value && t("update:modelValue", e.modelValue + 1)
                }

                return {
                    pagination: n,
                    updatePageHandler: c,
                    isPrevControlsActive: o,
                    isNextControlsActive: i,
                    goToFirst: l,
                    goToLast: r,
                    goToPrev: s,
                    goToNext: u
                }
            }
        });
        const z = Object(a["N"])("data-v-2a30deb0");
        Object(a["x"])("data-v-2a30deb0");
        const S = {class: "Pagination"}, _ = {key: 0, class: "PaginationControl"}, M = {class: "PaginationControl"},
            R = {class: "PaginationControl"}, E = {key: 1, class: "PaginationControl"};
        Object(a["v"])();
        const H = z((e, t, n, c, o, i) => {
            const l = Object(a["C"])("icon-page-first"), s = Object(a["C"])("icon-chevron-left"),
                r = Object(a["C"])("v-page"), u = Object(a["C"])("icon-chevron-right"),
                p = Object(a["C"])("icon-page-last");
            return Object(a["u"])(), Object(a["e"])("ul", S, [e.hideFirstButton ? Object(a["f"])("v-if", !0) : (Object(a["u"])(), Object(a["e"])("li", _, [Object(a["k"])(l, {
                class: ["Control", {"Control-active": e.isPrevControlsActive}],
                onClick: e.goToFirst
            }, null, 8, ["class", "onClick"])])), Object(a["k"])("li", M, [Object(a["k"])(s, {
                class: ["Control", {"Control-active": e.isPrevControlsActive}],
                onClick: e.goToPrev
            }, null, 8, ["class", "onClick"])]), (Object(a["u"])(!0), Object(a["e"])(a["a"], null, Object(a["A"])(e.pagination, t => (Object(a["u"])(), Object(a["e"])(r, {
                key: "pagination-page-" + t,
                page: t,
                current: e.modelValue,
                "active-color": e.activeColor,
                onUpdate: e.updatePageHandler
            }, null, 8, ["page", "current", "active-color", "onUpdate"]))), 128)), Object(a["k"])("li", R, [Object(a["k"])(u, {
                class: ["Control", {"Control-active": e.isNextControlsActive}],
                onClick: e.goToNext
            }, null, 8, ["class", "onClick"])]), e.hideLastButton ? Object(a["f"])("v-if", !0) : (Object(a["u"])(), Object(a["e"])("li", E, [Object(a["k"])(p, {
                class: ["Control", {"Control-active": e.isNextControlsActive}],
                onClick: e.goToLast
            }, null, 8, ["class", "onClick"])]))])
        });
        N.render = H, N.__scopeId = "data-v-2a30deb0", N.__file = "src/components/VPagination.vue";
        var I = N, U = (n("42d8"), {
            components: {AddTweet: p["a"], Tweet: b["a"], VPagination: I},
            data: function () {
                return {tweetData: [], page: 1, allTweetsCount: 10}
            },
            computed: Object(u["a"])(Object(u["a"])({}, Object(d["b"])(["getMe"])), Object(d["c"])(["isPaginationEnabled", "paginationLimit"])),
            watch: {
                isPaginationEnabled: function () {
                    this.getTweets()
                }
            },
            mounted: function () {
                var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
                    return regeneratorRuntime.wrap((function (e) {
                        while (1) switch (e.prev = e.next) {
                            case 0:
                                this.getTweets();
                            case 1:
                            case "end":
                                return e.stop()
                        }
                    }), e, this)
                })));

                function t() {
                    return e.apply(this, arguments)
                }

                return t
            }(),
            methods: {
                onPaginate: function () {
                    this.getTweets()
                }, handleTweetSubmit: function () {
                    var e = this;
                    return Object(r["a"])(regeneratorRuntime.mark((function t() {
                        return regeneratorRuntime.wrap((function (t) {
                            while (1) switch (t.prev = t.next) {
                                case 0:
                                    return t.prev = 0, t.next = 3, e.getTweets();
                                case 3:
                                    t.next = 8;
                                    break;
                                case 5:
                                    t.prev = 5, t.t0 = t["catch"](0), e.$notification({
                                        type: "error",
                                        message: "Error in send tweet"
                                    });
                                case 8:
                                case "end":
                                    return t.stop()
                            }
                        }), t, null, [[0, 5]])
                    })))()
                }, getTweets: function () {
                    var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
                        var t, n, a, c, o, i;
                        return regeneratorRuntime.wrap((function (e) {
                            while (1) switch (e.prev = e.next) {
                                case 0:
                                    if (!this.isPaginationEnabled) {
                                        e.next = 10;
                                        break
                                    }
                                    return e.next = 3, Object(g["d"])();
                                case 3:
                                    return i = e.sent, this.allTweetsCount = null === i || void 0 === i || null === (c = i.data) || void 0 === c || null === (o = c.tweets) || void 0 === o ? void 0 : o.length, e.next = 7, Object(g["e"])(this.page, this.paginationLimit);
                                case 7:
                                    a = e.sent, e.next = 13;
                                    break;
                                case 10:
                                    return e.next = 12, Object(g["d"])();
                                case 12:
                                    a = e.sent;
                                case 13:
                                    this.tweetData = null === (t = a) || void 0 === t || null === (n = t.data) || void 0 === n ? void 0 : n.tweets;
                                case 14:
                                case "end":
                                    return e.stop()
                            }
                        }), e, this)
                    })));

                    function t() {
                        return e.apply(this, arguments)
                    }

                    return t
                }(), handleTweetDelete: function () {
                    var e = this;
                    return Object(r["a"])(regeneratorRuntime.mark((function t() {
                        return regeneratorRuntime.wrap((function (t) {
                            while (1) switch (t.prev = t.next) {
                                case 0:
                                    e.handleTweetSubmit();
                                case 1:
                                case "end":
                                    return t.stop()
                            }
                        }), t)
                    })))()
                }
            }
        });
        n("a9bc");
        U.render = s;
        t["default"] = U
    }
}]);
//# sourceMappingURL=chunk-0420bcc4.11441662.js.map