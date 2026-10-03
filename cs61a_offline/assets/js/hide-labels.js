// 三套独立规则：阅读栏始终显示；参考答案由 VISIBLE_ANSWERS 控制；其余标签由 VISIBLE_LECTURES 控制。
// 第几讲 = 该周内从上到下第几行（1 开始）。
var VISIBLE_LECTURES = [
  { week: 1, lecture: 1 },
];

var VISIBLE_ANSWERS = [
];

$(function () {
  $('a.label-outline').hide();

  function isAnswer() {
    return $(this).text().trim() === '参考答案';
  }

  // 1) 「阅读」栏始终显示
  $('#calendar tr').each(function () {
    var $row = $(this);
    var $reading = $row.children('td').not('.weeknum').eq(1); // 第 2 个非周次 td = 阅读
    $reading.find('a.label-outline').show();
  });

  // 建立 周次 -> 该周所有行（按讲课顺序）的映射
  var weekRows = {};
  $('td.weeknum').each(function () {
    var $cell = $(this);
    var n = parseInt($cell.text().trim(), 10);
    if (!n) return;
    var rowspan = parseInt($cell.attr('rowspan'), 10) || 1;
    var rows = [];
    var $row = $cell.closest('tr');
    rows.push($row);
    $row.nextAll('tr').slice(0, rowspan - 1).each(function () {
      rows.push($(this));
    });
    weekRows[n] = rows;
  });

  function rowOf(item) {
    var rows = weekRows[item.week];
    return rows && rows[item.lecture - 1] ? rows[item.lecture - 1] : $();
  }

  // 2) 「参考答案」单独白名单
  VISIBLE_ANSWERS.forEach(function (item) {
    rowOf(item).find('a.label-outline').filter(isAnswer).show();
  });

  // 3) 其余标签白名单（排除参考答案）
  VISIBLE_LECTURES.forEach(function (item) {
    rowOf(item).find('a.label-outline').not(isAnswer).show();
  });
});
