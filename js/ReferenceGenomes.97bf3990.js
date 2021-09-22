(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["ReferenceGenomes"],{"1d18":function(e,t,r){},"20a9":function(e,t,r){"use strict";var n=r("1d18"),a=r.n(n);a.a},4430:function(e,t,r){"use strict";r.r(t);var n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("b-container",{staticClass:"galaxy-reference-genomes"},[r("b-row",[r("b-input-group",{attrs:{size:"sm",prepend:"Filter"}},[r("b-form-input",{attrs:{value:e.filter,type:"search",placeholder:"Type to Search"},on:{input:e.update_filter}}),r("b-input-group-append",[r("b-button",{attrs:{disabled:!e.filter},on:{click:function(t){e.filter=""}}},[e._v("Clear")])],1)],1)],1),r("b-table",{ref:"table",attrs:{hover:"",small:"",borderless:"",selectable:"","show-empty":"","select-mode":"single",items:e.genomes,busy:e.isLoading,fields:[{key:"name",sortable:!0}],"current-page":e.currentPage,"per-page":e.perPage,filter:e.filter,"filter-function":e.filterFunc,"primary-key":"id","thead-class":"hidden_header"},on:{"row-selected":e.row_selected}},[r("template",{slot:"table-busy"},[r("div",{staticClass:"text-center"},[r("b-spinner",{staticClass:"align-middle"}),r("strong",[e._v("Loading...")])],1)])],2),r("b-row",{attrs:{"align-h":"center"}},[r("b-pagination",{attrs:{"per-page":e.perPage,"total-rows":e.totalRows,limit:"8"},model:{value:e.currentPage,callback:function(t){e.currentPage=t},expression:"currentPage"}})],1)],1)},a=[],i=(r("a4d3"),r("e01a"),r("d28b"),r("4de4"),r("caad"),r("b0c0"),r("a9e3"),r("d3b7"),r("2532"),r("3ca3"),r("ddb0"),r("3835")),l=(r("96cf"),r("1da1")),s=r("f281"),o={name:"ReferenceGenomes",props:{perPage:{type:Number,default:10},value:{type:String,default:""},filter_delay:{type:Number,default:500}},data:function(){return{currentPage:1,filter:"",filter_delay_handle:null}},methods:{row_selected:function(e){e.length?this.$emit("input",e[0]):this.$emit("input",null)},clearSelected:function(){this.$refs.table.clearSelected(),this.$emit("input",null)},filterFunc:function(e,t){return e.name.toLowerCase().includes(t)},update_filter:function(e){null!==this.filter_delay_handle&&window.clearTimeout(this.filter_delay_handle),this.filter_delay_handle=window.setTimeout((function(t){return t.filter=e.toLowerCase()}),this.filter_delay,this)}},computed:{totalRows:function(){return this.genomes.length},isLoading:function(){return 0===this.genomes.length}},asyncComputed:{genomes:{get:function(){var e=Object(l["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(t=s["Genome"].query().orderBy("name").get(),0!==t.length){e.next=5;break}return e.next=4,s["Genome"].fetch();case 4:t=s["Genome"].query().orderBy("name").get();case 5:return e.abrupt("return",t);case 6:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}(),default:[]}},mounted:function(){if(this.value){var e=!0,t=!1,r=void 0;try{for(var n,a=this.genomes().elements()[Symbol.iterator]();!(e=(n=a.next()).done);e=!0){var l=Object(i["a"])(n.value,2),s=l[0],o=l[1];if(this.value===o.id){this.$refs.table.selectRow(s);break}}}catch(u){t=!0,r=u}finally{try{e||null==a.return||a.return()}finally{if(t)throw r}}}}},u=o,c=(r("20a9"),r("2877")),f=Object(c["a"])(u,n,a,!1,null,null,null);t["default"]=f.exports},a9e3:function(e,t,r){"use strict";var n=r("83ab"),a=r("da84"),i=r("94ca"),l=r("6eeb"),s=r("5135"),o=r("c6b6"),u=r("7156"),c=r("c04e"),f=r("d039"),d=r("7c73"),p=r("241c").f,h=r("06cf").f,b=r("9bf2").f,g=r("58a8").trim,m="Number",y=a[m],w=y.prototype,_=o(d(w))==m,v=function(e){var t,r,n,a,i,l,s,o,u=c(e,!1);if("string"==typeof u&&u.length>2)if(u=g(u),t=u.charCodeAt(0),43===t||45===t){if(r=u.charCodeAt(2),88===r||120===r)return NaN}else if(48===t){switch(u.charCodeAt(1)){case 66:case 98:n=2,a=49;break;case 79:case 111:n=8,a=55;break;default:return+u}for(i=u.slice(2),l=i.length,s=0;s<l;s++)if(o=i.charCodeAt(s),o<48||o>a)return NaN;return parseInt(i,n)}return+u};if(i(m,!y(" 0o1")||!y("0b1")||y("+0x1"))){for(var N,I=function(e){var t=arguments.length<1?0:e,r=this;return r instanceof I&&(_?f((function(){w.valueOf.call(r)})):o(r)!=m)?u(new y(v(t)),r,I):v(t)},E=n?p(y):"MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger".split(","),k=0;E.length>k;k++)s(y,N=E[k])&&!s(I,N)&&b(I,N,h(y,N));I.prototype=w,w.constructor=I,l(a,m,I)}}}]);
//# sourceMappingURL=ReferenceGenomes.97bf3990.js.map