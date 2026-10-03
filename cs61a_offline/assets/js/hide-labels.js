// 「讲座与考试 / 实验与讨论 / 作业与项目 / 小测」四栏同步由 VISIBLE_LECTURES 控制；
// 「阅读」栏始终显示；「参考答案」单独由 VISIBLE_ANSWERS 控制。
// 未开放的行，实验与讨论 / 作业与项目 / 小测 三栏的链接不可点击。
// 第几讲 = 该周内从上到下第几行（1 开始）。
var VISIBLE_LECTURES = [ { week: 1, lecture: 1 } ];
var VISIBLE_ANSWERS   = [ ];

$(function () {
  $('a.label-outline').hide();

  function isAnswer() { return $(this).text().trim() === '参考答案'; }

  function cellOf($row, col) {
    return $row.children('td').not('.weeknum').eq(col);
  }

  // 阅读栏始终显示
  $('#calendar tr').each(function () {
    cellOf($(this), 1).find('a.label-outline').show();
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
    $row.nextAll('tr').slice(0, rowspan - 1).each(function () { rows.push($(this)); });
    weekRows[n] = rows;
  });

  function rowOf(item) {
    var rows = weekRows[item.week];
    return rows && rows[item.lecture - 1] ? rows[item.lecture - 1] : $();
  }

  // 锁定/解锁链接（锁定 = 移除 href 并标记，不可点击）
  function lockLinks($scope) {
    $scope.find('a').each(function () {
      var $a = $(this);
      $a.attr('data-original-href', $a.attr('href') || '')
        .removeAttr('href')
        .addClass('label-locked');
    });
  }
  function unlockLinks($scope) {
    $scope.find('a.label-locked').each(function () {
      var $a = $(this);
      $a.attr('href', $a.attr('data-original-href'))
        .removeClass('label-locked')
        .removeAttr('data-original-href');
    });
  }

  // 未开放的行：禁用 实验(2)/作业(3)/小测(4) 三栏的链接
  var openRows = {};
  VISIBLE_LECTURES.forEach(function (item) { openRows[item.week + '-' + item.lecture] = true; });
  Object.keys(weekRows).forEach(function (w) {
    weekRows[w].forEach(function ($row, idx) {
      var lecture = idx + 1;
      if (openRows[w + '-' + lecture]) return;
      lockLinks(cellOf($row, 2).add(cellOf($row, 3)).add(cellOf($row, 4)));
    });
  });

  // 四栏同步显示：讲座与考试 / 实验与讨论 / 作业与项目 / 小测（排除参考答案）
  VISIBLE_LECTURES.forEach(function (item) {
    rowOf(item).find('a.label-outline').not(isAnswer).show();
  });

  // 参考答案单独白名单：显示并保持可点击
  VISIBLE_ANSWERS.forEach(function (item) {
    var $answers = rowOf(item).find('a.label-outline').filter(isAnswer);
    $answers.show();
    unlockLinks($answers);
  });

  // 清空位：隐藏没有任何可见链接的 ul.list-inline，避免残留空白
  $('#calendar ul.list-inline').each(function () {
    if ($(this).find('a:visible').length === 0) {
      $(this).hide();
    }
  });

  // 锁定样式：不可点击
  $('<style>').text(
    'a.label-locked{pointer-events:none;color:#999;text-decoration:none;cursor:default;}'
  ).appendTo('head');
});
