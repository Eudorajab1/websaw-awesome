(function(){
"use strict";
var ՐՏ_2;
function ՐՏ_extends(child, parent) {
    child.prototype = Object.create(parent.prototype);
    child.prototype.__base__ = parent;
    child.prototype.constructor = child;
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
    var ՐՏitr4, ՐՏidx4;
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
        ՐՏitr4 = ՐՏ_Iterable(a);
        for (ՐՏidx4 = 0; ՐՏidx4 < ՐՏitr4.length; ՐՏidx4++) {
            i = ՐՏitr4[ՐՏidx4];
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
ՐՏ_modules.ՐՏ_def("asset.rs_vue");
ՐՏ_modules.ՐՏ_def("asset");

ՐՏ_modules["ՐՏ:asset.rs_vue"].body = function(){
    var __name__ = "asset.rs_vue";

    function is_hook(name) {
        return [ "beforeCreate", "created", "beforeMount", "mounted", "beforeUpdate", "updated", "activated", "deactivated", "beforeDestroy", "destroyed", "render" ].includes(name);
    }
    function is_special(name) {
        return /^(_.+|constructor)$/.test(name);
    }
    class RS_vue {
        constructor (v_collector, name) {
            var ՐՏ_1, ՐՏitr1, ՐՏidx1, ՐՏitr2, ՐՏidx2, ՐՏitr3, ՐՏidx3;
            var self = this;
            var tmp, bases, it, sym, _name, k, methods, meth;
            if (!v_collector) {
                v_collector = self.__vue_opt__;
            } else if (ՐՏ_type(v_collector) === "String") {
                name = v_collector;
                v_collector = self.__vue_opt__;
            }
            if (name) {
                self.name = (ՐՏ_1 = name.split("."))[ՐՏ_1.length-1];
            }
            self.props = {};
            if (tmp = self.data || self._init_data) {
                self.data = tmp;
            }
            self.methods = {};
            if (v_collector) {
                if ((bases = v_collector.bases) && bases.length) {
                    self.mixins = v_collector.bases.map(function(it) {
                        if (it instanceof RS_vue) {
                            return it;
                        }
                        return new it();
                    });
                }
                self.computed = v_collector._computed;
                self.directives = v_collector._directives;
                self.filters = v_collector._filters;
                self.watch = v_collector._watch;
                Object.assign(self.methods, v_collector._methods);
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
            methods = Object.getOwnPropertyDescriptors(self.__proto__);
            ՐՏitr3 = ՐՏ_Iterable(methods);
            for (ՐՏidx3 = 0; ՐՏidx3 < ՐՏitr3.length; ՐՏidx3++) {
                meth = ՐՏitr3[ՐՏidx3];
                if (is_special(meth) || v_collector && v_collector.__collected__[meth]) {
                    continue;
                }
                if (is_hook(meth)) {
                    self[meth] = methods[meth].value;
                } else if (methods[meth].value.call) {
                    self.methods[meth] = methods[meth].value;
                }
            }
        }
        static make () {
            var args = [].slice.call(arguments, 0);
            var cls;
            cls = this;
            return new cls(...args);
        }
    }
    function unpack_name_fun_opt(f_reg_as) {
        function unpacker(reg_as, name_fun_opt, opt) {
            var self, arg1type, name;
            self = this;
            if (!name_fun_opt) {
                if (reg_as === "_getters") {
                    return function(f) {
                        var name;
                        name = f.__name__ || f.name;
                        return f_reg_as.call(self, reg_as, name, f());
                    };
                } else {
                    throw new Error("Attempt to call V_Collector @decorator with empty `()`");
                }
            }
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
    var V_collector = (ՐՏ_2 = class V_collector {
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
            self.__current__ = null;
            self.__collected__ = {};
        }
        _collector (opt_name, extra) {
            var self = this;
            self.__current__ = {
                __collected__: {}
            };
            if (extra) {
                Object.assign(self.__current__, extra);
            }
            function wrapper(cls) {
                cls.prototype[opt_name] = self.__current__;
                cls.prototype.name = cls.name;
                self.__current__ = null;
                return cls;
            }
            return wrapper;
        }
        component () {
            var self = this;
            var bases = [].slice.call(arguments, 0);
            return self._collector("__vue_opt__", {
                bases: bases
            });
        }
        store () {
            var self = this;
            return self._collector("__store_opt__");
        }
        _reg_as (reg_as, name, fun_opt) {
            var self = this;
            var cur;
            cur = self.__current__ || self;
            if (!cur[reg_as]) {
                cur[reg_as] = {};
            }
            cur[reg_as][name] = fun_opt;
            cur.__collected__[name] = true;
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
        model (name_or_fun) {
            var self = this;
            return self._reg_as("_getters")(name_or_fun);
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
        Object.defineProperties(ՐՏ_2.prototype, {
            _reg_as: {
                enumerable: false, 
                writable: true, 
                value: unpack_name_fun_opt(ՐՏ_2.prototype._reg_as)
            }
        });
        return ՐՏ_2;
    })(), ՐՏ_2);
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.rs_vue"];
    ՐՏ_mod.export("is_hook", function(){return is_hook;}, function(ՐՏ_v){if (typeof is_hook !== "undefined") {is_hook = ՐՏ_v;};});
    ՐՏ_mod.export("is_special", function(){return is_special;}, function(ՐՏ_v){if (typeof is_special !== "undefined") {is_special = ՐՏ_v;};});
    ՐՏ_mod.export("RS_vue", function(){return RS_vue;}, function(ՐՏ_v){if (typeof RS_vue !== "undefined") {RS_vue = ՐՏ_v;};});
    ՐՏ_mod.export("unpack_name_fun_opt", function(){return unpack_name_fun_opt;}, function(ՐՏ_v){if (typeof unpack_name_fun_opt !== "undefined") {unpack_name_fun_opt = ՐՏ_v;};});
    ՐՏ_mod.export("V_collector", function(){return V_collector;}, function(ՐՏ_v){if (typeof V_collector !== "undefined") {V_collector = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset"].body = function(){
    var __name__ = "asset";

    ՐՏ_modules["ՐՏ:asset"].export("rs_vue", function(){return ՐՏ_modules["asset.rs_vue"];}, function(){throw new Error("use Object.defineProperty!");});

    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset"];
    return ՐՏ_mod["exports"];
};

(function(){

    var __name__ = "__main__";

    var ՐՏ_3;
    var templ, vc;
    templ = "\n<form  class = 'chat-box' @submit = 'on_submit = $event'/>\n<input  v-model = 'text' placeholder = 'Write a message' type = 'text'/>\n<button  :disabled = 'text === \"\"'>\n    Send\n</button>\n";
    var RS_vue = ՐՏ_modules["asset.rs_vue"].RS_vue;var V_collector = ՐՏ_modules["asset.rs_vue"].V_collector;
    vc = new V_collector();
    
    var ChatBox = (ՐՏ_3 = class ChatBox extends RS_vue {
        constructor () {
            super();
            var self = this;
            self.template = templ;
        }
        data () {
            var self = this;
            return {
                text: ""
            };
        }
        on_submit () {
            var self = this;
            self.$emit("submit", self.text);
            self.text = "";
        }
        load () {
            var self = this;
            self.messages = [ "Welocme", "How", "Are", "You" ];
        }
        created () {
            var self = this;
            self.load();
        }
    }, ՐՏ_3 = vc.component()((function(){
        Object.defineProperties(ՐՏ_3.prototype, {
            on_submit: {
                enumerable: false, 
                writable: true, 
                value: vc.meth(ՐՏ_3.prototype.on_submit)
            }
        });
        return ՐՏ_3;
    })()), ՐՏ_3);
    function make() {
        return new ChatBox();
    }
})();
})();
