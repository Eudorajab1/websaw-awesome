(function(){
"use strict";
var ՐՏ_1;
function ՐՏ_extends(child, parent) {
    child.prototype = Object.create(parent.prototype);
    child.prototype.__base__ = parent;
    child.prototype.constructor = child;
}
function ՐՏ_in(val, arr) {
    if (typeof arr.indexOf === "function") {
        return arr.indexOf(val) !== -1;
    } else if (typeof arr.has === "function") {
        return arr.has(val);
    }
    return arr.hasOwnProperty(val);
}
function ՐՏ_Iterable(iterable) {
    var tmp;
    if (iterable.constructor === [].constructor || iterable.constructor === "".constructor || (tmp = Array.prototype.slice.call(iterable)).length) {
        return tmp || iterable;
    }
    if (Set && iterable.constructor === Set) {
        return Array.from(iterable);
    }
    return Object.keys(iterable);
}
function range(start, stop, step) {
    var length, idx, range;
    if (arguments.length <= 1) {
        stop = start || 0;
        start = 0;
    }
    step = arguments[2] || 1;
    length = Math.max(Math.ceil((stop - start) / step), 0);
    idx = 0;
    range = new Array(length);
    while (idx < length) {
        range[idx++] = start;
        start += step;
    }
    return range;
}
function ՐՏ_type(obj) {
    return obj && obj.constructor && obj.constructor.name ? obj.constructor.name : Object.prototype.toString.call(obj).slice(8, -1);
}
function ՐՏ_eq(a, b) {
    var ՐՏitr9, ՐՏidx9;
    var i;
    if (a === b) {
        return true;
    }
    if (a === void 0 || b === void 0 || a === null || b === null) {
        return false;
    }
    if (a.constructor !== b.constructor) {
        return false;
    }
    if (Array.isArray(a)) {
        if (a.length !== b.length) {
            return false;
        }
        for (i = 0; i < a.length; i++) {
            if (!ՐՏ_eq(a[i], b[i])) {
                return false;
            }
        }
        return true;
    } else if (a.constructor === Object) {
        if (Object.keys(a).length !== Object.keys(b).length) {
            return false;
        }
        ՐՏitr9 = ՐՏ_Iterable(a);
        for (ՐՏidx9 = 0; ՐՏidx9 < ՐՏitr9.length; ՐՏidx9++) {
            i = ՐՏitr9[ՐՏidx9];
            if (!ՐՏ_eq(a[i], b[i])) {
                return false;
            }
        }
        return true;
    } else if (Set && a.constructor === Set || Map && a.constructor === Map) {
        if (a.size !== b.size) {
            return false;
        }
        for (i of a) {
            if (!b.has(i)) {
                return false;
            }
        }
        return true;
    } else if (a.constructor === Date) {
        return a.getTime() === b.getTime();
    } else if (typeof a.__eq__ === "function") {
        return a.__eq__(b);
    }
    return false;
}
function ՐՏ_def_modules() {
    var modules;
    modules = {};
    function mounter(mod_id) {
        var rs_mod_id, rs_mod;
        rs_mod_id = "ՐՏ:" + mod_id;
        rs_mod = modules[rs_mod_id] = {
            "body": null,
            "exports": null
        };
        rs_mod["export"] = function(prop, get, set) {
            if (!rs_mod["exports"]) {
                rs_mod["exports"] = {};
            }
            Object.defineProperty(rs_mod["exports"], prop, {
                configurable: true,
                enumerable: true,
                get: get,
                set: set
            });
        };
        Object.defineProperty(modules, mod_id, {
            enumerable: true,
            get: function() {
                var mod;
                return (mod = modules[rs_mod_id])["exports"] || mod["body"]();
            },
            set: function(v) {
                modules[rs_mod_id]["exports"] = v;
            }
        });
        return rs_mod;
    }
    Object.defineProperty(modules, "ՐՏ_def", {
        configurable: false,
        enumerable: false,
        value: mounter
    });
    return modules;
}
var ՐՏ_modules = ՐՏ_def_modules();
ՐՏ_modules.ՐՏ_def("asset.common");
ՐՏ_modules.ՐՏ_def("asset.rs_vue");
ՐՏ_modules.ՐՏ_def("asset");

ՐՏ_modules["ՐՏ:asset.common"].body = function(){
    var __name__ = "asset.common";

    function asyncer(fun) {
        var ctx, ret;
        ctx = {
            self: void 0,
            args: void 0
        };
        function pret(ok, err) {
            function inner(f, ret_v, ret_throw) {
                var v;
                if (ret_throw) {
                    v = ret_throw;
                } else {
                    try {
                        f = f || fun.apply(ctx.self, ctx.args);
                        v = f.next(ret_v);
                    } catch (ՐՏ_Exception) {
                        var e = ՐՏ_Exception;
                        err(e);
                        return;
                    }
                }
                if (!v.done) {
                    if (v.value instanceof Promise) {
                        v.value.then(function(ret_v) {
                            inner(f, ret_v);
                        }, function(e) {
                            var v;
                            try {
                                v = f.throw(e);
                            } catch (ՐՏ_Exception) {
                                var e = ՐՏ_Exception;
                                err(e);
                                return;
                            }
                            inner(f, null, v);
                        });
                    } else {
                        Promise.resolve(v.value).then(function(ret_v) {
                            inner(f, ret_v);
                        });
                    }
                } else {
                    ok(v.value);
                }
            }
            inner();
        }
        ret = function() {
            ctx.self = this;
            ctx.args = arguments;
            return new Promise(pret);
        };
        ret.__name__ = fun.__name__ || fun.name;
        return ret;
    }
    function upload_text() {
        function prom(ok, err) {
            var el, ret;
            el = document.createElement("input");
            el.setAttribute("type", "file");
            el.setAttribute("multiple", true);
            el.style.display = "none";
            document.body.appendChild(el);
            ret = [];
            el.onchange = function() {
                var done, i, fr;
                done = el.files.length;
                for (i = 0; i < el.files.length; i++) {
                    fr = new FileReader();
                    fr._filename_ = el.files[i].name;
                    fr.onloadend = function(s) {
                        ret.push({
                            name: s.target._filename_,
                            value: s.target.result
                        });
                        --done;
                        if (done === 0) {
                            ok(ret);
                        }
                    };
                    fr.readAsText(el.files[i]);
                }
            };
            el.click();
            document.body.removeChild(el);
        }
        return new Promise(prom);
    }
    function download(s, filename, mime) {
        var blob, el_data, el;
        blob = new Blob([ s ], {
            type: mime || "text/plain;charset=utf-8;"
        });
        el_data = window.URL.createObjectURL(blob);
        el = document.createElement("a");
        el.setAttribute("href", el_data);
        el.setAttribute("download", filename);
        el.style.display = "none";
        document.body.appendChild(el);
        el.click();
        document.body.removeChild(el);
        window.URL.revokeObjectURL(blob);
    }
    function SF(text, props) {
        function replacer(str_, p) {
            var t, p_chain;
            if (t = /^("|')(.+?)("|')$/.exec(p)) {
                return props[t[2]];
            }
            if ((p_chain = p.split(".")) && p_chain.length > 1) {
                return p_chain.reduce(function(it, p) {
                    return it[p];
                }, props);
            }
            return props[p];
        }
        return text.replace(/\$\{ *(.+?) *\}/g, replacer);
    }
    function make_drag_listener(catcher, debounce) {
        var ctx;
        ctx = {
            catcher: catcher,
            x0: 0,
            y0: 0,
            dx: 0,
            dy: 0,
            vc: null,
            debounce: debounce || 50,
            move_done: null
        };
        function mousemove(e) {
            function process_move() {
                ctx.dx = e.clientX - ctx.x0;
                ctx.dy = e.clientY - ctx.y0;
                ctx.catcher.call(null, "drag_move", e, {
                    dx: ctx.dx,
                    dy: ctx.dy,
                    vc: ctx.vc
                });
                ctx.move_done = true;
            }
            e.stopPropagation();
            e.preventDefault();
            if (ctx.move_done === null) {
                process_move();
            } else if (ctx.move_done) {
                ctx.move_done = false;
                setTimeout(process_move, ctx.debounce);
            }
        }
        function mouseup(e) {
            document.removeEventListener("mousemove", mousemove);
            document.removeEventListener("mouseup", mouseup);
            e.stopPropagation();
            e.preventDefault();
            ctx.catcher.call(null, "drag_stop", e, {
                dx: ctx.dx,
                dy: ctx.dy,
                vc: ctx.vc
            });
        }
        function mousedn(e) {
            ctx.vc = this;
            ctx.x0 = e.clientX;
            ctx.y0 = e.clientY;
            if (!ctx.catcher) {
                ctx.catcher = function(what, e, args) {
                    ctx.vc.$emit(what, e, args);
                };
            }
            document.addEventListener("mousemove", mousemove, false);
            document.addEventListener("mouseup", mouseup, false);
            e.stopPropagation();
            e.preventDefault();
            ctx.catcher.call(null, "drag_start", e, {
                x0: ctx.x0,
                y0: ctx.y0,
                vc: ctx.vc
            });
        }
        return mousedn;
    }
    function blur_click_listener(el, cb) {
        var ret, blur;
        ret = {};
        blur = false;
        function doc_click_cap(e) {
            blur = true;
            setTimeout(function() {
                blur && cb(e);
            }, 0);
        }
        function el_click(e) {
            blur = false;
        }
        ret.start = function() {
            document.addEventListener("click", doc_click_cap, true);
            el.addEventListener("click", el_click, true);
        };
        ret.stop = function() {
            document.removeEventListener("click", doc_click_cap, true);
            el.removeEventListener("click", el_click, true);
        };
        return ret;
    }
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.common"];
    ՐՏ_mod.export("asyncer", function(){return asyncer;}, function(ՐՏ_v){if (typeof asyncer !== "undefined") {asyncer = ՐՏ_v;};});
    ՐՏ_mod.export("upload_text", function(){return upload_text;}, function(ՐՏ_v){if (typeof upload_text !== "undefined") {upload_text = ՐՏ_v;};});
    ՐՏ_mod.export("download", function(){return download;}, function(ՐՏ_v){if (typeof download !== "undefined") {download = ՐՏ_v;};});
    ՐՏ_mod.export("SF", function(){return SF;}, function(ՐՏ_v){if (typeof SF !== "undefined") {SF = ՐՏ_v;};});
    ՐՏ_mod.export("make_drag_listener", function(){return make_drag_listener;}, function(ՐՏ_v){if (typeof make_drag_listener !== "undefined") {make_drag_listener = ՐՏ_v;};});
    ՐՏ_mod.export("blur_click_listener", function(){return blur_click_listener;}, function(ՐՏ_v){if (typeof blur_click_listener !== "undefined") {blur_click_listener = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset.rs_vue"].body = function(){
    var __name__ = "asset.rs_vue";

    function print_log() {
        var args = [].slice.call(arguments, 0);
        if (window.ENV && window.ENV.debug) {
            console.log.apply(console, arguments);
        }
    }
    function find_recursive(obj, cb, max_iter) {
        var i, ctx, ret;
        max_iter = max_iter || 1e3;
        i = 0;
        ctx = {};
        ret = cb.call(ctx, obj, i);
        while (!ret[1] && i < max_iter) {
            ret = cb.call(ctx, ret[0], i);
            ++i;
        }
        if (i >= max_iter) {
            throw new Error("max iteration exceeded");
        }
        return ret[0];
    }
    function make_prop_chain(path, prefix, splitter) {
        prefix = prefix || "";
        splitter = splitter || ".";
        return path.split(splitter).filter(function(v) {
            return v;
        }).reduce(function(p, v) {
            return p + prefix + "." + v;
        }, "");
    }
    function make_prop_getter(prop_chain) {
        var me, ret;
        me = make_prop_getter;
        if (!(ret = me._memo[prop_chain])) {
            ret = me._memo[prop_chain] = new Function("obj", "{return obj" + prop_chain + "}");
        }
        return ret;
    }
    make_prop_getter._memo = {};
    function split_modgetter_rest(store, path) {
        var self, mod_rest, modgetter;
        self = store;
        mod_rest = /(^(\/[\w$]+)+)((\.[^.]+)+)$/.exec(path);
        if (!mod_rest) {
            return [ function() {
                return self;
            }, path ];
        } else {
            modgetter = make_prop_getter(make_prop_chain(mod_rest[1].slice(1), ".modules", "/"));
        }
        return [ modgetter, mod_rest[3].slice(1) ];
    }
    function unpack_name_fun_opt(f_reg_as) {
        function unpacker(reg_as, name_fun_opt, opt) {
            var self, arg1type, name;
            if (!name_fun_opt) {
                throw new Error("Attempt to call V_Collector @decorator with empty `()`");
            }
            self = this;
            arg1type = ՐՏ_type(name_fun_opt);
            if (arg1type.startsWith("Fun")) {
                name = name_fun_opt.__name__ || name_fun_opt.name;
                return f_reg_as.call(self, reg_as, name, name_fun_opt);
            } else {
                return function(f) {
                    var name;
                    if (arg1type.startsWith("Str")) {
                        name = name_fun_opt;
                        if (opt) {
                            opt.handler = f;
                        } else {
                            opt = f;
                        }
                    } else {
                        opt = name_fun_opt;
                        name = f.__name__ || f.name;
                        opt.handler = f;
                    }
                    return f_reg_as.call(self, reg_as, name, opt);
                };
            }
        }
        return unpacker;
    }
    var V_collector = (ՐՏ_1 = class V_collector {
        constructor () {
            var self = this;
            self._methods = null;
            self._computed = null;
            self._watch = null;
            self._filters = null;
            self._directives = null;
            self._getters = null;
            self._mutations = null;
            self._actions = null;
        }
        _reg_as (reg_as, name, fun_opt) {
            var self = this;
            print_log("reg " + reg_as + " " + name + " self: ", self);
            if (!self[reg_as]) {
                self[reg_as] = {};
            }
            self[reg_as][name] = fun_opt;
            return fun_opt.handler ? fun_opt.handler : fun_opt;
        }
        meth (name_or_fun) {
            var self = this;
            return self._reg_as("_methods", name_or_fun);
        }
        computed (name_or_fun) {
            var self = this;
            return self._reg_as("_computed", name_or_fun);
        }
        filter (name_or_fun) {
            var self = this;
            return self._reg_as("_filters", name_or_fun);
        }
        directive (name_or_fun) {
            var self = this;
            return self._reg_as("_directives", name_or_fun);
        }
        watch (name_or_fun, opt) {
            var self = this;
            return self._reg_as("_watch", name_or_fun, opt);
        }
        getter (name_or_fun) {
            var self = this;
            return self._reg_as("_getters", name_or_fun);
        }
        mutation (name_or_fun) {
            var self = this;
            return self._reg_as("_mutations", name_or_fun);
        }
        action (name_or_fun) {
            var self = this;
            return self._reg_as("_actions", name_or_fun);
        }
    }, (function(){
        Object.defineProperties(ՐՏ_1.prototype, {
            _reg_as: {
                enumerable: false, 
                writable: true, 
                value: unpack_name_fun_opt(ՐՏ_1.prototype._reg_as)
            }
        });
        return ՐՏ_1;
    })(), ՐՏ_1);
    class RS_vue {
        constructor (v_collector) {
            var ՐՏitr1, ՐՏidx1, ՐՏitr2, ՐՏidx2, ՐՏitr3, ՐՏidx3;
            var self = this;
            var it, sym, _name, k, self_keys, v_spec, tmp;
            self.props = {};
            self.data = self._init_data;
            self.delimiters = [ "{{", "}}" ];
            if (v_collector) {
                self.methods = v_collector._methods;
                self.computed = v_collector._computed;
                self.directives = v_collector._directives;
                self.filters = v_collector._filters;
                self.watch = v_collector._watch;
                ՐՏitr1 = ՐՏ_Iterable([ [ "~", "_mutations" ], [ "*", "_actions" ] ]);
                for (ՐՏidx1 = 0; ՐՏidx1 < ՐՏitr1.length; ՐՏidx1++) {
                    it = ՐՏitr1[ՐՏidx1];
                    [sym, _name] = it;
                    if (v_collector[_name]) {
                        if (!self.map_store) {
                            self.map_store = {};
                        }
                        ՐՏitr2 = ՐՏ_Iterable(v_collector[_name]);
                        for (ՐՏidx2 = 0; ՐՏidx2 < ՐՏitr2.length; ՐՏidx2++) {
                            k = ՐՏitr2[ՐՏidx2];
                            self.map_store[k] = sym;
                            self.methods[k] = v_collector[_name][k];
                        }
                    }
                }
            }
            self_keys = Object.keys(self);
            ՐՏitr3 = ՐՏ_Iterable([ "beforeCreate", "created", "beforeMount", "mounted", "beforeUpdate", "updated", "activated", "deactivated", "beforeDestroy", "destroyed" ]);
            for (ՐՏidx3 = 0; ՐՏidx3 < ՐՏitr3.length; ՐՏidx3++) {
                v_spec = ՐՏitr3[ՐՏidx3];
                if (!(ՐՏ_in(v_spec, self_keys)) && (tmp = self.__proto__[v_spec])) {
                    self[v_spec] = tmp;
                }
            }
        }
        _init_data () {
            var self = this;
            throw ReferenceError("Not implemented");
        }
    }
    class RS_state_api {
        constructor (vc, vue, state, vm_opt) {
            var ՐՏitr4, ՐՏidx4;
            var self = this;
            var get_prop, getter_name;
            self.vue = vue;
            self.raw_getters = vc._getters;
            self.mutations = vc._mutations;
            vm_opt = Object.assign({}, vm_opt || {}, {
                data: {
                    state: state
                },
                computed: self.raw_getters,
                map_store: vc._map_store
            });
            self.vm = new vue(vm_opt);
            self.vm.rs_state_api = self;
            self.state = self.vm.state;
            self.getters = {};
            get_prop = Object.getOwnPropertyDescriptor;
            if (self.raw_getters) {
                ՐՏitr4 = ՐՏ_Iterable(self.raw_getters);
                for (ՐՏidx4 = 0; ՐՏidx4 < ՐՏitr4.length; ՐՏidx4++) {
                    getter_name = ՐՏitr4[ՐՏidx4];
                    self.getters[getter_name] = get_prop(self.vm, getter_name).get;
                }
            }
        }
        commit (mutation) {
            var self = this;
            var payload = [].slice.call(arguments, 1);
            var h;
            print_log("mutation: ", mutation);
            print_log("\tpayload: ", payload);
            if (h = self.mutations[mutation]) {
                return h.apply(self, payload);
            } else {
                throw new Error("unknown mutation: " + mutation);
            }
        }
        $del () {
            var self = this;
            self.vm.$delete.apply(self.vm, arguments);
        }
        $set () {
            var self = this;
            self.vm.$set.apply(self.vm, arguments);
        }
        check_path (path) {
            var self = this;
            var last_prnt;
            path = path.split(".");
            if (path.length === 1) {
                return self.state.hasOwnProperty(path[0]);
            }
            try {
                last_prnt = path.slice(0, -1).reduce(function(s, name) {
                    return s[name];
                }, self.state);
            } catch (ՐՏ_Exception) {
                if (ՐՏ_Exception instanceof TypeError) {
                    return false;
                } else {
                    throw ՐՏ_Exception;
                }
            }
            return last_prnt.hasOwnProperty(path[path.length-1]);
        }
        _get (path) {
            var self = this;
            return make_prop_getter(make_prop_chain(path))(self.vm.state);
        }
        get (path) {
            var self = this;
            if (self.getters.hasOwnProperty(path)) {
                return self.vm[path];
            } else {
                return self._get(path);
            }
        }
        set_getter (h, as_name) {
            var self = this;
            var v, getter;
            as_name = as_name || h.__name__ || h.name;
            if (!(as_name && ՐՏ_type(as_name).startsWith("Str"))) {
                throw new Error("can`t get the name of new getter: " + h);
            }
            if (as_name === "state") {
                throw new Error("`state` is bad name for new getter: " + h);
            }
            v = new self.vue({
                computed: {
                    [as_name]: function() {
                        return h.call(self.vm);
                    }
                }
            });
            getter = Object.getOwnPropertyDescriptor(v, as_name);
            Object.defineProperty(self.vm, as_name, getter);
            self.getters[as_name] = getter.get;
        }
        set_mutation (h, as_name) {
            var self = this;
            as_name = as_name || h.__name__ || h.name;
            if (!(as_name && ՐՏ_type(as_name).startsWith("Str"))) {
                throw new Error("can`t get the name of new mutation: " + h);
            }
            if (ՐՏ_in(as_name, self.mutations)) {
            } else if (self.hasOwnProperty(as_name)) {
                throw new Error("Bad mutation name: " + as_name);
            }
            self.mutations[as_name] = self[as_name] = h;
        }
    }
    class RS_store {
        constructor () {
            var self = this;
            if (!self.vue) {
                throw ReferenceError("You should first call Vue.use(Your_Store)");
            }
            self.dispatch_bound = function() {
                return self.dispatch.apply(self, arguments);
            };
            self.commit_bound = function() {
                return self.commit.apply(self, arguments);
            };
            self.$bus = {
                $on: function(e, cb) {
                    return self.$on(e, cb);
                },
                $off: function(e, cb) {
                    self.$off(e, cb);
                },
                $emit: function() {
                    var args = [].slice.call(arguments, 0);
                    self.$emit(...args);
                }
            };
        }
        mount_module (mod_obj, as_name) {
            var self = this;
            as_name = as_name || mod_obj.__name__ || mod_obj.constructor && mod_obj.constructor.name;
            if (!(as_name && ՐՏ_type(as_name).startsWith("Str"))) {
                throw new Error("can`t get the name of module: " + mod_obj);
            }
            if (self.state_api.state.hasOwnProperty(as_name)) {
                throw new Error("can`t mount module under name `" + as_name + "`,  name already exists");
            }
            if (!self.modules) {
                self.modules = {};
            }
            self.modules[as_name] = mod_obj;
            self.state_api.$set(self.state_api.state, as_name, mod_obj.state_api.state);
        }
        replace_state (new_state) {
            var ՐՏitr5, ՐՏidx5;
            var self = this;
            var _new_state, k, it, mod;
            _new_state = {};
            ՐՏitr5 = ՐՏ_Iterable(new_state);
            for (ՐՏidx5 = 0; ՐՏidx5 < ՐՏitr5.length; ՐՏidx5++) {
                k = ՐՏitr5[ՐՏidx5];
                it = new_state[k];
                if (self.modules && (mod = self.modules[k])) {
                    it = mod.replace_state(it);
                }
                _new_state[k] = it;
            }
            self.state_api.$set(self.state_api.vm, "state", _new_state);
            self.state_api.state = self.state_api.vm.state;
            return self.state_api.state;
        }
        _get (path) {
            var self = this;
            var mod, rest;
            [mod, rest] = split_modgetter_rest(self, path);
            return mod(self).state_api._get(rest);
        }
        get (path) {
            var self = this;
            var mod, rest;
            [mod, rest] = split_modgetter_rest(self, path);
            return mod(self).state_api.get(rest);
        }
        getter_factory (path) {
            var self = this;
            var argtype, modgetter, rest, getter;
            argtype = ՐՏ_type(path);
            if (argtype[0] === "S") {
                [modgetter, rest] = split_modgetter_rest(self, path);
            } else if (argtype[0] === "F") {
                modgetter = arguments[0];
                rest = arguments[1];
            } else {
                throw new Error("Wrong args: ", arguments);
            }
            getter = make_prop_getter(make_prop_chain(rest));
            return function() {
                var mod;
                mod = modgetter(self);
                if (mod.state_api.getters.hasOwnProperty(rest)) {
                    return mod.state_api.vm[rest];
                } else {
                    return getter(mod.state_api.vm.state);
                }
            };
        }
        handler_factory (path) {
            var self = this;
            var modgetter, rest, mutation, action;
            [modgetter, rest] = split_modgetter_rest(self, path);
            if (rest.endsWith("~")) {
                mutation = rest.slice(0, -1);
                return function() {
                    var args = [].slice.call(arguments, 0);
                    modgetter(self).state_api.commit(mutation, ...args);
                };
            } else if (rest.endsWith("*")) {
                action = rest.slice(0, -1);
                return function() {
                    var args = [].slice.call(arguments, 0);
                    return modgetter(self)._dispatch(action, ...args);
                };
            } else {
                return self.getter_factory(modgetter, rest);
            }
        }
        $on (e, cb) {
            var self = this;
            self.state_api.vm.$on(e, cb);
            return function() {
                self.$off(e, cb);
            };
        }
        $off (e, cb) {
            var self = this;
            self.state_api.vm.$off(e, cb);
        }
        $emit () {
            var self = this;
            self.state_api.vm.$emit.apply(self.state_api.vm, arguments);
        }
        commit (mutation) {
            var self = this;
            var payload = [].slice.call(arguments, 1);
            var modgetter;
            [modgetter, mutation] = split_modgetter_rest(self, mutation);
            return modgetter(self).state_api.commit(mutation, ...payload);
        }
        _dispatch (action) {
            var self = this;
            var payload = [].slice.call(arguments, 1);
            var p;
            print_log("action: ", action);
            print_log("\tpayload: ", payload);
            if (!self.actions || !(ՐՏ_in(action, self.actions))) {
                throw new Error("unknown action: " + action);
            }
            p = self[action].apply(self, payload);
            if (!(p instanceof Promise)) {
                p = Promise.resolve(p);
            }
            return p;
        }
        dispatch (action) {
            var self = this;
            var payload = [].slice.call(arguments, 1);
            var modgetter, mod;
            [modgetter, action] = split_modgetter_rest(self, action);
            mod = modgetter(self);
            return mod._dispatch(action, ...payload);
        }
        set_action (h, as_name) {
            var self = this;
            as_name = as_name || h.__name__ || h.name;
            if (!(as_name && ՐՏ_type(as_name).startsWith("Str"))) {
                throw new Error("can`t get the name of new action: " + h);
            }
            if (ՐՏ_in(as_name, self.actions)) {
            } else if (self.hasOwnProperty(as_name)) {
                throw new Error("Bad action name: " + as_name);
            }
            self.actions[as_name] = self[as_name] = h;
        }
        static before_create () {
            var ՐՏitr6, ՐՏidx6, ՐՏitr8, ՐՏidx8;
            var map_store, is_mutation_re, is_action_re, $opts, $map_opts, self, injectors, opt, k, map_to, map_from, map_to_split, map_to_meth, store_meth, modgetter, rest, store_mod, handler, action, mutation;
            map_store = "map_store";
            is_mutation_re = /(.+)~$/;
            is_action_re = /(.+)\*$/;
            $opts = this.$options;
            $map_opts = $opts[map_store] || $opts.propsData && $opts.propsData[map_store];
            if (!$map_opts) {
                return;
            }
            self = $opts.store || function(vm) {
                var tmp, store;
                tmp = find_recursive(vm, function(o) {
                    return [ o.$parent, !o.$parent || o.$parent.$options.store ];
                });
                store = tmp.$options.store;
                if (!store) {
                    throw ReferenceError("store not found");
                }
                return store;
            }(this);
            injectors = {
                "*": function(f) {
                    return function() {
                        f.call(this, self.dispatch_bound, ...arguments);
                    };
                },
                "~": function(f) {
                    return function() {
                        f.call(this, self.commit_bound, ...arguments);
                    };
                }
            };
            ՐՏitr6 = ՐՏ_Iterable([ "methods", "computed" ]);
            for (ՐՏidx6 = 0; ՐՏidx6 < ՐՏitr6.length; ՐՏidx6++) {
                opt = ՐՏitr6[ՐՏidx6];
                $opts[opt] = Object.assign({}, $opts[opt]);
            }
            if (Array.isArray($map_opts)) {
                $map_opts = (function() {
                    var ՐՏidx7, ՐՏitr7 = ՐՏ_Iterable($map_opts), ՐՏres = {}, k;
                    for (ՐՏidx7 = 0; ՐՏidx7 < ՐՏitr7.length; ՐՏidx7++) {
                        k = ՐՏitr7[ՐՏidx7];
                        ՐՏres[k] = k;
                    }
                    return ՐՏres;
                })();
            }
            ՐՏitr8 = ՐՏ_Iterable($map_opts);
            for (ՐՏidx8 = 0; ՐՏidx8 < ՐՏitr8.length; ՐՏidx8++) {
                map_to = ՐՏitr8[ՐՏidx8];
                map_from = $map_opts[map_to];
                if (ՐՏ_in(map_from, [ "*", "~" ])) {
                    if (!$opts.methods[map_to]) {
                        throw ReferenceError("Can`t map " + map_from + " to non-existing method: " + map_to);
                    }
                    $opts.methods[map_to] = injectors[map_from]($opts.methods[map_to]);
                } else if (ՐՏ_type(map_from).startsWith("Fun") && (map_to_split = /(.+?)(\*|~)$/.exec(map_to))) {
                    map_to_meth = map_to_split[1];
                    store_meth = map_to_split[2];
                    $opts.methods[map_to_meth] = injectors[store_meth](map_from);
                } else {
                    [modgetter, rest] = split_modgetter_rest(self, map_from);
                    store_mod = modgetter(self);
                    if (rest === "$bus") {
                        $opts["computed"][map_to] = function() {
                            return modgetter(self).$bus;
                        };
                        continue;
                    }
                    handler = self.handler_factory(map_from);
                    if (action = is_action_re.exec(rest)) {
                        action = action[1];
                        if (!(ՐՏ_in(action, store_mod.actions))) {
                            throw ReferenceError("unknown action in `map_store`: " + map_from);
                        }
                        if ($opts["methods"][map_to]) {
                            $opts["methods"][map_to] = function(h, store_h) {
                                return function() {
                                    return h.call(this, store_h, ...arguments);
                                };
                            }($opts["methods"][map_to], handler);
                        } else {
                            $opts["methods"][map_to] = handler;
                        }
                    } else if (mutation = is_mutation_re.exec(rest)) {
                        mutation = mutation[1];
                        if (!(ՐՏ_in(mutation, store_mod.state_api.mutations))) {
                            throw ReferenceError("unknown mutation in `map_store`: " + map_from);
                        }
                        if ($opts["methods"][map_to]) {
                            $opts["methods"][map_to] = function(h, store_h) {
                                return function() {
                                    return h.call(this, store_h, ...arguments);
                                };
                            }($opts["methods"][map_to], handler);
                        } else {
                            $opts["methods"][map_to] = handler;
                        }
                    } else if (ՐՏ_in(rest, store_mod.state_api.getters) || store_mod.state_api.check_path(rest)) {
                        $opts["computed"][map_to] = handler;
                    } else {
                        throw ReferenceError("Can`t map `" + map_from + "` to `" + map_to + "`");
                    }
                }
            }
        }
        static beforeDestroy () {
            var self;
            self = this;
            if (self.bus_cleanup && self.bus_cleanup.length) {
                print_log("bus_cleanup", self.bus_cleanup);
                self.bus_cleanup.forEach(function(off) {
                    off();
                });
            }
        }
        static install (Vue, opt) {
            RS_store.prototype.vue = Vue;
            Vue.mixin({
                beforeCreate: RS_store.before_create,
                beforeDestroy: RS_store.beforeDestroy
            });
        }
    }
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.rs_vue"];
    ՐՏ_mod.export("print_log", function(){return print_log;}, function(ՐՏ_v){if (typeof print_log !== "undefined") {print_log = ՐՏ_v;};});
    ՐՏ_mod.export("find_recursive", function(){return find_recursive;}, function(ՐՏ_v){if (typeof find_recursive !== "undefined") {find_recursive = ՐՏ_v;};});
    ՐՏ_mod.export("make_prop_chain", function(){return make_prop_chain;}, function(ՐՏ_v){if (typeof make_prop_chain !== "undefined") {make_prop_chain = ՐՏ_v;};});
    ՐՏ_mod.export("make_prop_getter", function(){return make_prop_getter;}, function(ՐՏ_v){if (typeof make_prop_getter !== "undefined") {make_prop_getter = ՐՏ_v;};});
    ՐՏ_mod.export("split_modgetter_rest", function(){return split_modgetter_rest;}, function(ՐՏ_v){if (typeof split_modgetter_rest !== "undefined") {split_modgetter_rest = ՐՏ_v;};});
    ՐՏ_mod.export("unpack_name_fun_opt", function(){return unpack_name_fun_opt;}, function(ՐՏ_v){if (typeof unpack_name_fun_opt !== "undefined") {unpack_name_fun_opt = ՐՏ_v;};});
    ՐՏ_mod.export("V_collector", function(){return V_collector;}, function(ՐՏ_v){if (typeof V_collector !== "undefined") {V_collector = ՐՏ_v;};});
    ՐՏ_mod.export("RS_vue", function(){return RS_vue;}, function(ՐՏ_v){if (typeof RS_vue !== "undefined") {RS_vue = ՐՏ_v;};});
    ՐՏ_mod.export("RS_state_api", function(){return RS_state_api;}, function(ՐՏ_v){if (typeof RS_state_api !== "undefined") {RS_state_api = ՐՏ_v;};});
    ՐՏ_mod.export("RS_store", function(){return RS_store;}, function(ՐՏ_v){if (typeof RS_store !== "undefined") {RS_store = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset"].body = function(){
    var __name__ = "asset";

    ՐՏ_modules["ՐՏ:asset"].export("common", function(){return ՐՏ_modules["asset.common"];}, function(){throw new Error("use Object.defineProperty!");});
    ՐՏ_modules["ՐՏ:asset"].export("rs_vue", function(){return ՐՏ_modules["asset.rs_vue"];}, function(){throw new Error("use Object.defineProperty!");});

    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset"];
    return ՐՏ_mod["exports"];
};

(function(){

    var __name__ = "__main__";

    var ՐՏ_2;
    var vc;
    var asyncer = ՐՏ_modules["asset.common"].asyncer;
    var v_meth = ՐՏ_modules["asset.rs_vue"].v_meth;var v_computed = ՐՏ_modules["asset.rs_vue"].v_computed;var v_watch = ՐՏ_modules["asset.rs_vue"].v_watch;var RS_vue = ՐՏ_modules["asset.rs_vue"].RS_vue;var V_collector = ՐՏ_modules["asset.rs_vue"].V_collector;
    vc = new V_collector();
    var App = (ՐՏ_2 = class App extends RS_vue {
        constructor () {
            super(vc);
            var self = this;
            self.el = "#vue";
        }
        _init_data () {
            var self = this;
            return {
                items: [],
                input: "",
                api: "/" + window.location.href.split("/")[3] + "/api"
            };
        }
        *load () {
            var self = this;
            var res;
            res = yield axios.get(self.api);
            self.items = res.data.items;
        }
        created () {
            var self = this;
            self.load();
        }
        *save (item_id) {
            var self = this;
            var res;
            res = yield axios.post(self.api, {
                info: self.input
            });
            if (self.input) {
                self.items.unshift({
                    id: res.data.id,
                    info: self.input
                });
            }
            self.input = "";
        }
        *remove (item_id) {
            var self = this;
            var idx;
            yield axios.delete(self.api + "/" + item_id);
            idx = self.items.findIndex(function(it) {
                var ՐՏ_3;
                return ((ՐՏ_3 = it.id) === item_id || typeof ՐՏ_3 === "object" && ՐՏ_eq(ՐՏ_3, item_id));
            });
            self.$delete(self.items, idx);
        }
    }, (function(){
        Object.defineProperties(ՐՏ_2.prototype, {
            load: {
                enumerable: false, 
                writable: true, 
                value: vc.meth(asyncer(ՐՏ_2.prototype.load))
            },
            save: {
                enumerable: false, 
                writable: true, 
                value: vc.meth(asyncer(ՐՏ_2.prototype.save))
            },
            remove: {
                enumerable: false, 
                writable: true, 
                value: vc.meth(asyncer(ՐՏ_2.prototype.remove))
            }
        });
        return ՐՏ_2;
    })(), ՐՏ_2);
    window.app = new Vue(new App());
})();
})();
