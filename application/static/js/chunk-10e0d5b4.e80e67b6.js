(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["chunk-10e0d5b4"], {
    "778c": function (e, n, r) {
    }, a55b: function (e, n, r) {
        "use strict";
        r.r(n);
        var t = r("7a23"), a = {class: "login"};

        function i(e, n, r, i, o, s) {
            return Object(t["u"])(), Object(t["g"])("div", a)
        }

        var o = r("1da1"), s = r("5530"), u = (r("96cf"), r("b0c0"), r("7424")), c = r("7f56"), d = r("5502"), l = {
            name: "LoginView", data: function () {
                return {
                    userInfo: {username: "kaanersoy", password: "password"},
                    validationError: {username: !1, password: !1}
                }
            }, computed: Object(s["a"])({}, Object(d["c"])(["currentUserApiKey"])), mounted: function () {
                this.handleLogin()
            }, methods: {
                handleLogin: function () {
                    var e = Object(o["a"])(regeneratorRuntime.mark((function e() {
                        var n, r, t, a, i, o;
                        return regeneratorRuntime.wrap((function (e) {
                            while (1) switch (e.prev = e.next) {
                                case 0:
                                    return e.prev = 0, e.next = 3, Object(u["h"])(this.userInfo, this.currentUserApiKey);
                                case 3:
                                    if (t = e.sent, t.data.user) {
                                        e.next = 6;
                                        break
                                    }
                                    return e.abrupt("return");
                                case 6:
                                    return a = t.data.user, i = new c["AvatarGenerator"], o = i.generateRandomAvatar(a.id), this.$store.dispatch("setLoginInfo", {
                                        id: a.id,
                                        username: a.name,
                                        profile: {
                                            pic: o,
                                            pic_full: o,
                                            pic_cover: "https://i.ibb.co/0G5ny1g/1500x500.jpg",
                                            description: "😎😎",
                                            nickname: a.name,
                                            name: a.name,
                                            website: "https://cooldev.com"
                                        },
                                        account: {
                                            followingCount: null === a || void 0 === a || null === (n = a.following) || void 0 === n ? void 0 : n.length,
                                            followerCount: null === a || void 0 === a || null === (r = a.followers) || void 0 === r ? void 0 : r.length
                                        }
                                    }), e.abrupt("return", this.$router.push("/"));
                                case 13:
                                    e.prev = 13, e.t0 = e["catch"](0), this.$notification({
                                        type: "error",
                                        message: "Failed when authentication"
                                    });
                                case 16:
                                case "end":
                                    return e.stop()
                            }
                        }), e, this, [[0, 13]])
                    })));

                    function n() {
                        return e.apply(this, arguments)
                    }

                    return n
                }(), validateForm: function () {
                    this.validationError.username = !1, this.validationError.password = !1, this.userInfo.username.length < 5 && (this.validationError.username = !0), this.userInfo.password.length < 5 && (this.validationError.password = !0)
                }
            }
        };
        r("fd47");
        l.render = i;
        n["default"] = l
    }, fd47: function (e, n, r) {
        "use strict";
        r("778c")
    }
}]);
//# sourceMappingURL=chunk-10e0d5b4.e80e67b6.js.map