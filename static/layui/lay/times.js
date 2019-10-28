!function (a) {
    // $("#sucaijiayuan").show()
    function b() {
        function p(a) {
            var b, c = 348;
            for (b = 32768; b > 8; b >>= 1) c += d[a - 1900] & b ? 1 : 0;
            return c + q(a)
        }

        function q(a) {
            return r(a) ? 15 == (15 & d[a - 1899]) ? 30 : 29 : 0
        }

        function r(a) {
            var b = 15 & d[a - 1900];
            return 15 == b ? 0 : b
        }

        function s(a, b) {
            return d[a - 1900] & 65536 >> b ? 30 : 29
        }

        function t(a, b) {
            return 1 == b ? 0 == a % 4 && 0 != a % 100 || 0 == a % 400 ? 29 : 28 : e[b]
        }

        function u(a) {
            return f[a % 10] + g[a % 12]
        }

        function v(a, b) {
            var c = new Date(31556925974.7 * (a - 1900) + 6e4 * k[b] + Date.UTC(1900, 0, 6, 2, 5));
            return 2016 == a && 22 == b ? c.getUTCDate() + 1 : c.getUTCDate()
        }

        function x(a) {
            var b, c = 0, d = 0,
                e = (Date.UTC(a.getFullYear(), a.getMonth(), a.getDate()) - Date.UTC(1900, 0, 31)) / 864e5;
            for (b = 1900; 2100 > b && e > 0; b++) d = p(b), e -= d;
            for (0 > e && (e += d, b--), this.year = b, c = r(b), this.isLeap = !1, b = 1; 13 > b && e > 0; b++) c > 0 && b == c + 1 && 0 == this.isLeap ? (--b, this.isLeap = !0, d = q(this.year)) : d = s(this.year, b), 1 == this.isLeap && b == c + 1 && (this.isLeap = !1), e -= d;
            0 == e && c > 0 && b == c + 1 && (this.isLeap ? this.isLeap = !1 : (this.isLeap = !0, --b)), 0 > e && (e += d, --b), this.month = b, this.day = e + 1
        }

        function y(a, b, c, d, e, f, g, h, i, j, k) {
            this.isToday = !1, this.sYear = a, this.sMonth = b, this.sDay = c, this.week = d, this.lYear = e, this.lMonth = f, this.lDay = g, this.isLeap = h, this.cYear = i, this.cMonth = j, this.cDay = k, this.color = "", this.lunarFestival = "", this.solarFestival = "", this.solarTerms = ""
        }

        function z(a, b) {
            var d, e, f, h, k, m, p, r, w, L, M, N, R, S, T, U, g = 1, i = 0, O = new Array(3), P = 0, Q = 0,
                c = new Date(a, b, 1, 0, 0, 0, 0);
            for (this.length = t(a, b), this.firstWeek = c.getDay(), L = 2 > b ? u(a - 1900 + 36 - 1) : u(a - 1900 + 36), R = v(a, 2), S = v(a, 2 * b), M = u(12 * (a - 1900) + b + 12), p = 12 * (a - 1900) + b + 12, T = Date.UTC(a, b, 1, 0, 0, 0, 0) / 864e5 + 25567 + 10, U = 0; U < this.length; U++) g > i && (c = new Date(a, b, U + 1), d = new x(c), e = d.year, f = d.month, g = d.day, h = d.isLeap, i = h ? q(e) : s(e, f), 0 == P && (Q = f), O[P++] = U - g + 1), 1 == b && U + 1 == R && (L = u(a - 1900 + 36), r = a - 1900 + 36), U + 1 == S && (M = u(12 * (a - 1900) + b + 13), p = 12 * (a - 1900) + b + 13), N = u(T + U), w = T + U, this[U] = new y(a, b + 1, U + 1, l[(U + this.firstWeek) % 7], e, f, g++, h, L, M, N);
            k = v(a, 2 * b) - 1, m = v(a, 2 * b + 1) - 1, this[k].solarTerms = j[2 * b], this[m].solarTerms = j[2 * b + 1], 3 == b && (this[k].color = "red");
            for (U in n) n[U].match(/^(\d{2})(\d{2})([\s\*])(.+)$/) && Number(RegExp.$1) == b + 1 && (this[Number(RegExp.$2) - 1].solarFestival += RegExp.$4 + "  ", "*" == RegExp.$3 && (this[Number(RegExp.$2) - 1].color = "red"));
            for (U in o) o[U].match(/^(\d{2})(.{2})([\s\*])(.+)$/) && (k = Number(RegExp.$1) - Q, -11 == k && (k = 1), k >= 0 && P > k && (m = O[k] + Number(RegExp.$2) - 1, m >= 0 && m < this.length && (this[m].lunarFestival += RegExp.$4 + "  ", "*" == RegExp.$3 && (this[m].color = "red"))));
            a == G && b == H && (this[I - 1].isToday = !0)
        }

        function A(a) {
            var b;
            switch (a) {
                case 10:
                    b = "初十";
                    break;
                case 20:
                    b = "二十";
                    break;
                case 30:
                    b = "三十";
                    break;
                default:
                    b = m[Math.floor(a / 10)], b += l[a % 10]
            }
            return b
        }

        function D(a, c) {
            var d, e, f, i, j;
            for (B = new z(a, c), $("#GZ")[0].innerHTML = "  农历" + u(a - 1900 + 36) + "年&nbsp;【" + h[(a - 4) % 12] + "年】", d = 0; 42 > d; d++)
                sObj = $("#SD" + d)[0],
                    lObj = $("#LD" + d)[0],
                    sObj.className = "",
                    e = d - B.firstWeek,
                    e > -1 && e < B.length ? (sObj.innerHTML = e + 1,
                        $("#GD" + d).unbind("click").click(function () {
                            b = "s.", V(this, e + 1)
                        }),

                        $("#GD" + d).attr("on", "0"),
                        i = a + "" + X(c + 1) + X(e + 1),
                        j = C.join(),

                    j.indexOf(i) > -1 && $("#GD" + d).addClass("selday"),
                    B[e].isToday && $("#GD" + d).addClass("jinri"),
                        sObj.style.color = B[e].color,
                        lObj.innerHTML = 1 == B[e].lDay ? '<b style="font-weight:normal;font-size:10px;">' + (B[e].isLeap ? "闰" : "") + B[e].lMonth + "月" + (29 == s(B[e].lYear, B[e].lMonth) ? "小" : "大") + "</b>" : A(B[e].lDay),
                        f = B[e].lunarFestival, f.length > 0 ? (f.length > 8 && (f = f.substr(0, 5) + "..."), f = f.fontcolor("red")) : (f = B[e].solarFestival, f.length > 0 ? (f.length > 8 && (f = f.substr(0, 5) + "..."),
                        f = "黑色星期五" == f ? f.fontcolor("black") : f.fontcolor("#0066FF")) : (f = B[e].solarTerms, f.length > 0 && (f = f.fontcolor("limegreen")))), "清明" == B[e].solarTerms && (f = "清明节".fontcolor("red")),
                    "芒种" == B[e].solarTerms && (f = "芒种".fontcolor("red")),
                    "夏至" == B[e].solarTerms && (f = "夏至".fontcolor("red")),
                    "冬至" == B[e].solarTerms && (f = "冬至".fontcolor("red")),
                    f.length > 0 && (lObj.innerHTML = f)) : ($("#GD" + d).addClass("unover"), $("#GD" + d).unbind("click"))
        }

        function E() {
            for (i = 0; 42 > i; i++) sObj = $("#SD" + i)[0], sObj.innerHTML = "", lObj = $("#LD" + i)[0], lObj.innerHTML = "", $("#GD" + i).removeClass("unover"), $("#GD" + i).removeClass("jinri"),
                $("#GD" + i).removeClass("selday")
        }

        function V(a) {
            function d() {
                var b = a.getElementsByTagName("font")[0],
                    d = "0",
                    e = $("#nian").text(),
                    f = $("#yue").text(),
                    g = b.innerHTML,
                    h = b.attributes["color"],
                    i = e + "/" + X(f) + "/" + X(g);
                h && "red" == h.value && Y(i) && (d = "1"), c = e + X(f) + X(g)
            }

            var e, c = "";
            d(),
                e = a.attributes["on"].value
            //点击时添加样式
            // "0" == e ? (a.setAttribute("class", "selday"),  a.attributes["on"].value = "1", C.push(c)) : (a.setAttribute("class", ""), a.attributes["on"].value = "0", W(C, c))
        }

        function W(a, b) {
            for (var c = a.length - 1; c > -1; c--) a[c] == b && a.splice(c, 1)
        }

        function X(a) {
            return 10 > a ? "0" + a : a
        }

        function Y(a) {
            var b = new Date(Date.parse(a)), c = b.getDay();
            return 0 == c || 6 == c ? !0 : !1
        }

        function bb() {
            var a = new Date;
            _.currYear = a.getFullYear(), _.currMonth = a.getMonth(), ab.init()
        }

        function cb() {
            bb(), E(), $("#nian").html(G), $("#yue").html(H + 1), D(G, H)
        }

        function db() {
            cb(),
                $("#nianjian").click(function () {
                    ab.goPrevYear()
                }),
                $("#nianjia").click(function () {
                    ab.goNextYear()
                }),
                $("#yuejian").click(function () {
                    ab.goPrevMonth()
                }),
                $("#yuejia").click(function () {
                    ab.goNextMonth()
                }),
                // $("#sucaijiayuan").hide(),
                $("#i_div").css("z-index", "0")
        }

        function eb() {
            return "" == C ? (alert("请至少选择一个日期！"), void 0) : ($("#i_div").css("z-index", "0"), $("#i_id").val(C), $(".btnQX").trigger("click"), void 0)
        }

        function fb() {
            $("#sucaijiayuan td").removeClass("selday").attr("on", 0), C = [], cb(), U = 0
            $("#trDa2 td").remove()
            $("#trDa td").remove()
            $("#trTime td ").remove()
            $("#trTime2 td").remove()
            $("#btnSave").css('display', 'none')

        }

        function gb() {
            // $("#sucaijiayuan").hide(),
            $("#i_div").css("z-index", "0")
        }

        function ib() {
            var a, b, c;
            for (b = 0; 6 > b; b++) {
                for (hb += '<tr align=center height="10px" id="tt" style="cursor:pointer ; -moz-user-select:-moz-none; -moz-user-select: none;-o-user-select:none;-khtml-user-select:none;-webkit-user-select:none;-ms-user-select:none;user-select:none;"  onselectstart="return false;">', c = 0; 7 > c; c++) a = 7 * b + c, hb += '<td class="major" id="GD' + a + '" on="0" ><font  id="SD' + a + '" style="font-size:14px;"  face="Arial"', 0 == c && (hb += "color=red"), 6 == c && (hb += 1 == b % 2 ? "color=red" : "color=red"), hb += '  TITLE="">  </font><br><font  id="LD' + a + '"  size=2  style="white-space:nowrap;overflow:hidden;"></font></td>';
                hb += "</tr>"
            }
        }

        var d, e, f, g, h, j, k, l, m, n, o, B, C, F, G, H, I, U, _, ab, hb, jb,
            a = "<div id='myrl' style='width: 100%'><form name='CLD'> " +
                " <TABLE class='biao' width='100%' height ='400px'  id='sucaijiayuan'>    " +
                " <TBODY id='t_body'>   " +
                " <TR>         " +
                " <TD class='calTit' colSpan=7 style='height:30px;padding-top:3px;text-align:center'>" +
                " <input type='button' value='提交' class='button6 btnTJ'>  " +
                " <input type='button' value='重置' class='button6 btnCZ'>      " +
                // " <input type='button' value='取消' class='button6 btnQX'>         " +
                " <div style='width:245px ;float:left'>                " +
                " <span id='dateSelectionRili' class='dateSelectionRili' style='cursor:pointer;color: white ' >        " +
                " <span id='nian' class='topDateFont'></span>  <span class='topDateFont'>年</span>    " +
                " <span id='yue' class='topDateFont'></span>     <span class='topDateFont'>月</span>   " +
                " <span class='dateSelectionBtn cal_next' >▼</span>   " + "    </span>  " +
                " <font id=GZ class='topDateFont'></font>   " + "   </div>      " +
                " <div style='float:left'>    " + "    <a href='#' title='上一年' id='nianjian' class='ymNaviBtn lsArrow'></a>     " +
                " <a href='#' title='上一月' id='yuejian' class='ymNaviBtn lArrow'></a>                        </div>     " +
                " <div style='width: 244px; height: 100px; top: 165px;display: none' id='dateSelectionDiv'>     " +
                " <div id='dateSelectionHeader'></div>             <div id='dateSelectionBody'> " +
                " <div id='yearList' style='left: 10px; position: relative;'>        " +
                " <div id='yearListPrev'>&lt</div>                   <div id='yearListContent'></div>      " +
                " <div id='yearListNext'>&gt</div>        </div>                " +
                " <div id='dateSeparator'></div>       <div id='monthList'>                 " +
                " <div id='monthListContent'>      </div>    " +
                " <div style='clear:both'></div>      </div>" +
                " <div id='dateSelectionBtn' style='position: relative;left: -7px;'>               " +
                " <div id='dateSelectionTodayBtn'>今天</div>       <div id='dateSelectionOkBtn'>确定</div> " +
                " <div id='dateSelectionCancelBtn'>取消</div>      </div>    " +
                " </div>  <div id='dateSelectionFooter'></div>    " +
                " </div>  <div style='float:right'>        " +
                " <a href='#' id='yuejia' title='下一月' class='ymNaviBtn rArrow'></a>     " +
                " <a href='#' id='nianjia' title='下一年' class='ymNaviBtn rsArrow'></a>             </div>                    </TD>  " +
                " </TR>  <TR class='calWeekTit' style='font-size:12px; height:20px;text-align:center'>            " +
                " <TD width='35' class='red'>星期日</TD>       <TD width='35'>星期一</TD>          <TD width='35'>星期二</TD>  " +
                " <TD width='35'>星期三</TD>       <TD width='35'>星期四</TD>        <TD width='35'>星期五</TD>   " +
                " <TD width='35' class='red'>星期六</TD>       </TR>   </tbody>              </TABLE>       " +
                " </form></div>",
            b = "Nope.", c = "";
        return document.getElementById("i_div").innerHTML = a,
            d = new Array(19416, 19168, 42352, 21717, 53856, 55632, 21844, 22191, 39632, 21970, 19168, 42422, 42192, 53840, 53845, 46415,
                54944, 44450, 38320, 18807, 18815, 42160, 46261, 27216, 27968, 43860, 11119, 38256, 21234, 18800, 25958, 54432, 59984, 27285,
                23263, 11104, 34531, 37615, 51415, 51551, 54432, 55462, 46431, 22176, 42420, 9695, 37584, 53938, 43344, 46423, 27808, 46416,
                21333, 19887, 42416, 17779, 21183, 43432, 59728, 27296, 44710, 43856, 19296, 43748, 42352, 21088, 62051, 55632, 23383, 22176,
                38608, 19925, 19152, 42192, 54484, 53840, 54616, 46400, 46752, 38310, 38335, 18864, 43380, 42160, 45690, 27216, 27968, 44870,
                43872, 38256, 19189, 18800, 25776, 29859, 59984, 27480, 23232, 43872, 38613, 37600, 51552, 55636, 54432, 55888, 30034, 22176,
                43959, 9680, 37584, 51893, 43344, 46240, 47780, 44368, 21977, 19360, 42416, 20854, 21183, 43312, 31060, 27296, 44368, 23378,
                19296, 42726, 42208, 53856, 60005, 54576, 23200, 30371, 38608, 19195, 19152, 42192, 53430, 53855, 54560, 56645, 46496, 22224,
                21938, 18864, 42359, 42160, 43600, 45653, 27951, 44448, 19299, 37759, 18936, 18800, 25776, 26790, 59999, 27424, 42692, 43759,
                37600, 53987, 51552, 54615, 54432, 55888, 23893, 22176, 42704, 21972, 21200, 43448, 43344, 46240, 46758, 44368, 21920, 43940,
                42416, 21168, 45683, 26928, 29495, 27296, 44368, 19285, 19311, 42352, 21732, 53856, 59752, 54560, 55968, 27302, 22239, 19168, 43476,
                42192, 53584, 62034, 54560), e = new Array(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),
            f = new Array("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"),
            g = new Array("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"),
            h = new Array("鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"),
            j = new Array("小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种",
                "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"),
            k = new Array(0, 21208, 42467, 63836, 85337, 107014, 128867, 150921, 173149, 195551, 218072, 240693, 263343,
                285989, 308563, 331033, 353350, 375494, 397447, 419210, 440795, 462224, 483532, 504758),
            l = new Array("日", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"),
            m = new Array("初", "十", "廿", "卅", " "),
            n = new Array("0101*元旦", "0501*劳动节", "1001*国庆节"),
            o = new Array("0101*春节", "0505*端午节", "0815*中秋节", "0100*除夕"),
            C = [], F = new Date, G = F.getFullYear(), H = F.getMonth(), I = F.getDate(), U = 0, _ = {
            currYear: -1,
            currMonth: -1,
            currDate: null,
            uid: null,
            username: null,
            email: null,
            single: !1
        }, ab = {
            currYear: -1,
            currMonth: -1,
            minYear: 1901,
            maxYear: 2100,
            beginYear: 0,
            endYear: 0,
            tmpYear: -1,
            tmpMonth: -1,
            init: function (a, b) {
                ("undefined" == typeof a || "undefined" == typeof b) && (a = _.currYear, b = _.currMonth), this.setYear(a), this.setMonth(b), this.showYearContent(), this.showMonthContent()
            },
            show: function () {
                document.getElementById("dateSelectionDiv").style.display = "block"
            },
            hide: function () {
                this.rollback(), document.getElementById("dateSelectionDiv").style.display = "none"
            },
            today: function () {
                var a = new Date, b = a.getFullYear(), c = a.getMonth();
                (this.currYear != b || this.currMonth != c) && (this.tmpYear == b && this.tmpMonth == c ? this.rollback() : (this.init(b, c), this.commit()))
            },
            go: function () {
                this.currYear == this.tmpYear && this.currMonth == this.tmpMonth ? this.rollback() : this.commit(), this.hide()
            },
            goToday: function () {
                this.today(), this.hide()
            },
            goPrevMonth: function () {
                this.prevMonth(), this.commit()
            },
            goNextMonth: function () {
                this.nextMonth(), this.commit()
            },
            goPrevYear: function () {
                this.prevYear(), this.commit()
            },
            goNextYear: function () {
                this.nextYear(), this.commit()
            },
            changeView: function () {
                _.currYear = this.currYear, _.currMonth = this.currMonth, E(), $("#nian").html(_.currYear), $("#yue").html(parseInt(_.currMonth) + 1), D(_.currYear, _.currMonth)
            },
            commit: function () {
                (-1 != this.tmpYear || -1 != this.tmpMonth) && ((this.currYear != this.tmpYear || this.currMonth != this.tmpMonth) && (this.showYearContent(), this.showMonthContent(), this.changeView()), this.tmpYear = -1, this.tmpMonth = -1)
            },
            rollback: function () {
                -1 != this.tmpYear && this.setYear(this.tmpYear), -1 != this.tmpMonth && this.setMonth(this.tmpMonth), this.tmpYear = -1, this.tmpMonth = -1, this.showYearContent(), this.showMonthContent()
            },
            prevMonth: function () {
                var b, a = this.currMonth - 1;
                -1 == a && (b = this.currYear - 1, b >= this.minYear ? (a = 11, this.setYear(b)) : a = 0), this.setMonth(a)
            },
            nextMonth: function () {
                var b, a = parseInt(this.currMonth) + 1;
                12 == a && (b = parseInt(this.currYear) + 1, b <= this.maxYear ? (a = 0, this.setYear(b)) : a = 11), this.setMonth(a)
            },
            prevYear: function () {
                var a = this.currYear - 1;
                a >= this.minYear && this.setYear(a)
            },
            nextYear: function () {
                var a = parseInt(this.currYear) + 1;
                a <= this.maxYear && this.setYear(a)
            },
            prevYearPage: function () {
                this.endYear = this.beginYear - 1, this.showYearContent(null, this.endYear)
            },
            nextYearPage: function () {
                this.beginYear = this.endYear + 1, this.showYearContent(this.beginYear, null)
            },
            selectYear: function () {
                var a = $('select[@name="SY"] option[@selected]').text();
                this.setYear(a), this.commit()
            },
            selectMonth: function () {
                var a = $('select[@name="SM"] option[@selected]').text();
                this.setMonth(a - 1), this.commit()
            },
            setYear: function (a) {
                -1 == this.tmpYear && -1 != this.currYear && (this.tmpYear = this.currYear), $("#SY" + this.currYear).removeClass("curr"), this.currYear = a, $("#SY" + this.currYear).addClass("curr")
            },
            setMonth: function (a) {
                -1 == this.tmpMonth && -1 != this.currMonth && (this.tmpMonth = this.currMonth), $("#SM" + this.currMonth).removeClass("curr"), this.currMonth = a, $("#SM" + this.currMonth).addClass("curr")
            },
            showYearContent: function (a, b) {
                var c, d;
                for (a || (b || (b = parseInt(this.currYear) + 1), this.endYear = b, this.endYear > this.maxYear && (this.endYear = this.maxYear), this.beginYear = this.endYear - 3, this.beginYear < this.minYear && (this.beginYear = this.minYear, this.endYear = this.beginYear + 3)), b || (a || (a = this.currYear - 2), this.beginYear = a, this.beginYear < this.minYear && (this.beginYear = this.minYear), this.endYear = this.beginYear + 3, this.endYear > this.maxYear && (this.endYear = this.maxYear, this.beginYear = this.endYear - 3)), c = "", d = this.beginYear; d <= this.endYear; d++) c += '<span id="SY' + d + '" class="year" >' + d + "</span>";
                document.getElementById("yearListContent").innerHTML = c, $("#SY" + this.currYear).addClass("curr"), $(".year").click(function () {
                    ab.setYear(this.id.replace("SY", ""))
                })
            },
            showMonthContent: function () {
                var b, a = "";
                for (b = 0; 12 > b; b++) a += '<span id="SM' + b + '" class="month">' + (b + 1).toString() + "</span>";
                document.getElementById("monthListContent").innerHTML = a, $(".month").click(function () {
                    var a = 0;
                    a = this.id.replace("SM", ""), ab.setMonth(a)
                }), $("#SM" + this.currMonth).addClass("curr")
            },
            goHoliday: function (a) {
                this.setMonth(a), this.commit()
            }
        }, hb = "", ib(),

            $(".btnTJ").click(function () {
                //平时加班天数
                var a = 0;
                //周6天数
                var b = 0;
                //节假日天数
                var c = 0;

                var Saturday = [];
                var FesDay = [];
                var usualDay = [];
                // 选择器  选择从第二个开始-不是最后一个
                var tr = $("tr:gt(1)").not(":last");
                var trLen = tr.length;
                //获取年月
                // 获取input 值是val(), 获取页面span...就是用html()
                var YM = $('#nian').html() + '-' + $('#yue').html();
                //计算周6 加班天数
                var arrFes = ['元旦', '劳动节', '国庆节', '春节', '端午节', '中秋节', '除夕', '清明节'];


                for (var i = 0; i < trLen; i++) {
                    var att = $(tr[i]).children('td').last().hasClass("selday");
                    if (att) {
                        //获取日期
                        var saDay = YM + '-' + $(tr[i]).children('td').last().find('font:first').html();
                        Saturday.push(saDay);
                        b++;
                    }

                    var tdOb = $(tr[i]).children('td').not(':last');
                    for (var j = 0; j < tdOb.length; j++) {
                        //。获取农历
                        var Fes = $(tdOb[j]).find('font:last').html();

                        // console.log(Fes);
                        if ($(tdOb[j]).hasClass("selday") && arrFes.includes(Fes.trim())) {
                            //是节假日
                            var day2 = $(tdOb[j]).find('font:first').html();
                            // console.log('11',day2);
                            FesDay.push(YM + '-' + day2);

                            c++
                            // console.log('12',c);


                        } else if ($(tdOb[j]).hasClass("selday") && !arrFes.includes(Fes.trim())) {
                            var day3 = $(tdOb[j]).find('font:first').html();
                            usualDay.push(YM + '-' + day3)
                            a++
                        }

                    }

                }

                var timeCount = a * 2 + b * 10 + c * 10;

                if (timeCount == 0) {
                    fb()
                } else {
                    var td1 = '';
                    var td2 = '';
                    var td3 = '';
                    var td4 = '';

                    function sortNumber(a, b) {
                        return a - b
                    }

                    for (var n = 0; n < usualDay.length; n++) {
                        td3 += '<td id="usualday" name="usualday" style="font-size: 12px">' + usualDay[n] + '</td>'
                        td4 += '<td>' + '2' + '</td>'
                    }

                    $('#trDa2').html('');
                    $('#trDa2').append(td3);
                    $('#trTime2').html('');
                    $('#trTime2').append(td4);

                    var FesSat = Saturday.concat(FesDay);
                    FesSat = FesSat.sort(sortNumber);
                    console.log(FesSat)
                    for (var m = 0; m < FesSat.length; m++) {
                        td1 += '<td id="saturday" name="saturday">' + FesSat[m] + '</td>'
                        td2 += '<td>' + '<input type="text" id="sat_id" name="sat" value="10">' + '</td>'
                    }
                    // console.log(td1);

                    $('#trDa').html('');
                    $('#trDa').append(td1).append('<td>' + '总计' + '</td>');
                    $('#trTime').html('');
                    $('#trTime').append(td2).append('<td id="tic" name="tic">' + timeCount + '</td>');

                    // $('#btnSave').attr(display = button)
                    $("#btnSave").css("display", "block");//修改display属性为block
                    $("#trTime").change(function () {


                        var count = 0;
                        var sat_count = $("#trTime > td > input ")
                        for (var sat = 0; sat < sat_count.length; sat++) {
                            count += parseInt($(sat_count[sat]).val())
                        }
                        $('#tic').html(count + a * 2)


                    });
                }
            }),

            $("#btnSave").click(function (e) {
                //平时加班天数
                var a = 0;
                //周6天数
                var b = 0;
                //节假日天数
                var c = 0;

                var Saturday = [];
                var FesDay = [];
                var usualDay = [];
                // 选择器  选择从第二个开始-不是最后一个
                var tr = $("tr:gt(1)").not(":last");
                var trLen = tr.length;
                //获取年月
                // 获取input 值是val(), 获取页面span...就是用html()
                var YM = $('#nian').html() + '-' + $('#yue').html();
                console.log('YM', YM)
                //计算周6 加班天数
                var arrFes = ['元旦', '劳动节', '国庆节', '春节', '端午节', '中秋节', '除夕', '清明节'];


                for (var i = 0; i < trLen; i++) {
                    var att = $(tr[i]).children('td').last().hasClass("selday");
                    if (att) {
                        //获取日期
                        var saDay = YM + '-' + $(tr[i]).children('td').last().find('font:first').html();
                        Saturday.push(saDay);
                        b++;
                    }

                    var tdOb = $(tr[i]).children('td').not(':last');
                    for (var j = 0; j < tdOb.length; j++) {
                        //。获取农历
                        var Fes = $(tdOb[j]).find('font:last').html();
                        if ($(tdOb[j]).hasClass("selday") && arrFes.includes(Fes.trim())) {
                            //是节假日
                            var day2 = $(tdOb[j]).find('font:first').html();
                            // console.log('11',day2);
                            FesDay.push(YM + '-' + day2);

                            c++
                        } else if ($(tdOb[j]).hasClass("selday") && !arrFes.includes(Fes.trim())) {
                            var day3 = $(tdOb[j]).find('font:first').html();
                            usualDay.push(YM + '-' + day3);
                            a++
                        }

                    }

                }
                var timeCount = $('#tic').html();
                // e.preventDefault();
                var data_time = {'fesDay[]': 0};
                var tname = parseInt($('#tname').val());
                if (tname >= timeCount) {
                    var sat_count = $("#trTime > td > input ");
                    var sat_value = $("#trDa > td");
                    // console.log('555', sat_value);
                    for (var sat = 0; sat < sat_count.length; sat++) {
                        console.log('--', $(sat_value[sat]).html());
                        data_time[$(sat_value[sat]).html()] = parseInt($(sat_count[sat]).val())
                        // }
                    }
                    for (var satid2 = 0; satid2 < usualDay.length; satid2++) {
                        console.log('--***', usualDay[satid2]);
                        data_time[usualDay[satid2]] = 2
                    }

                    data_time['tic'] = $('#tic').html();
                    data_time['fesDay'] = FesDay;
                    data_time['user_id'] = $('#user_id').val();
                    data_time['YM'] = YM;

                    // data_time['apply_id'] = $('#apply_id').val();
                    $.ajax({
                        type: $("#addTime").attr('method'),
                        url: "/dqe/overtime/ov/time/list",
                        data: data_time,
                        // cache: false,
                        dataType: "json",
                        success: function (msg) {
                            if (msg.result == 1) {
                                layer.alert('加班提报成功！', {icon: 1}, function (index) {
                                    parent.layer.closeAll(); //关闭所有弹窗
                                    window.location.href = "/dqe/overtime/ov/apply/list";
                                });
                            } else if (msg.result == 2) {
                                layer.alert('加班超过人数，請重新提拨 </br>' + '加班日期: [' + msg.day_Exceed + '] ', {
                                    title: '提示'
                                    , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                                    , time: 0 //不自动关闭
                                    , btn: ['YES']

                                });

                            } else if (msg.result == 3) {
                                layer.alert('错误原因:  </br>' + msg.message + '', {
                                    title: '提示'
                                    , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                                    , time: 0 //不自动关闭
                                    , btn: ['YES']

                                });
                            } else if (msg.result == 5) {
                                layer.alert('错误原因:  </br>' + msg.message + '', {
                                    title: '提示'
                                    , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                                    , time: 0 //不自动关闭
                                    , btn: ['YES']

                                });
                            } else if (msg.result == 6) {
                                layer.alert('错误原因:  </br>' + msg.message + '', {
                                    title: '提示'
                                    , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                                    , time: 0 //不自动关闭
                                    , btn: ['YES']

                                });
                            } else if (msg.result == 7) {
                                layer.alert('错误原因:  </br>' + msg.message + '', {
                                    title: '提示'
                                    , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                                    , time: 0 //不自动关闭
                                    , btn: ['YES']

                                });
                            } else if (msg.result == 4) {
                                layer.alert('还未到时间提报： </br>' + '错误原因: ' + msg.message + '', {
                                    title: '提示'
                                    , icon: 3 //0:感叹号 1：对号 2：差号 3：问号 4：小锁 5：哭脸 6：笑脸
                                    , time: 0 //不自动关闭
                                    , btn: ['YES']

                                });
                            }
                            return false;
                        }
                    });
                } else {
                    layer.alert('你提报的时数超过了' + tname + '小时')
                }

            }),


            $(".btnQX").click(function () {
                gb()
            }),

            $(".btnCZ").click(function () {
                fb()
            }), $(".cal_next").click(function () {
            ab.show()
        }), $(".dateSelectionRili").click(function () {
            ab.show()
        }), $("#dateSelectionTodayBtn").click(function () {
            ab.goToday()
        }), $("#dateSelectionOkBtn").click(function () {
            ab.go()
        }), $("#dateSelectionCancelBtn").click(function () {
            ab.hide()
        }), $("#yearListPrev").click(function () {
            ab.prevYearPage()
        }), $("#yearListNext").click(function () {
            ab.nextYearPage()
        }), $("#i_id").mouseover(function () {
            this.focus()
        }),
            $("#i_id").mouseout(function () {
                this.blur()
            }),
            $("#i_id").click(function () {
                console.log(123),
                    $("#sucaijiayuan").show(),

                    $("#i_div").css("z-index", "3"),
                    fb()
            }),


            $("#t_body").append(hb),
            $(".major").bind("contextmenu", function () {
                return !1
            }),
            $(".major").mousedown(function (a) {
                3 == a.which && (b = "Yeah.", c = $(this).attr("id"))
            }),

            //点击添加样式
            $("tr:gt(1)").not(":last").find('td:gt(0)').mousedown(function () {
                var tnumber = parseInt($('#tnumber').val());
                // console.log('111', tnumber)
                var f = 0;
                //获取这一行的td
                var num = $(this).parent().children('td');
                for (var j = 0; j < num.length; j++) {
                    if ($(num[j]).attr("class") == 'major selday' || $(num[j]).attr("class") == 'major jinri selday') {
                        f += 1;
                    }
                }

                if (f < tnumber) {
                    // console.log($(this).attr("class"));
                    if ($(this).attr("class") == 'major selday' || $(this).attr("class") == 'major jinri selday') {
                        $(this).removeClass('selday');
                    } else if ($(this).attr("class") == 'major' || $(this).attr("class") == 'major jinri') {
                        $(this).addClass("selday");
                    }

                } else if (f == tnumber && $(this).hasClass('selday')) {
                    $(this).removeClass("selday");
                } else {
                    alert("一周只能提报" + tnumber + "天");
                }


            }),
            $("html").mouseup(function () {
                b = "Nope."
            }),


            jb = {}, jb["initialization"] = db, jb
    }

    a.fn.LunarInitDate = function () {
        var a = b();
        a.initialization()
    }
}(jQuery);