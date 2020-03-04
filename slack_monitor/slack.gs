function Slack2SheetPost(jsonObj, score) {
  // スプレットシートに記述する
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('index');
  var newRow = sheet.getLastRow() + 1;

  sheet.getRange(newRow, 1).setValue(jsonObj["event_time"]); // タイムスタンプ
  sheet.getRange(newRow, 2).setValue(jsonObj["event_id"]); // イベントID
  sheet.getRange(newRow, 3).setValue(jsonObj["event"]["user"]); // ユーザーID
  sheet.getRange(newRow, 4).setValue(jsonObj["event"]["text"]); // 本文
  sheet.getRange(newRow, 5).setValue(score); // score
  sheet.getRange(newRow, 6).setValue(-1); // likes
  sheet.getRange(newRow, 7).setValue("Slack"); // slack or twitter
  var link = "https://dajarerits.slack.com/archives/" + jsonObj["event"]["channel"] + "/p";
  sheet.getRange(newRow, 8).setValue(link + jsonObj["event"]["ts"].replace('.','')); // link
  sheet.getRange(newRow, 9).setValue(""); // 備考
}

function SlackJoinEvent(jsonObj) {
  // slackのchannelに参加/退出イベントか判定する
  // この場合「<userid>~~~」という文字列がtextに入る

  var userId = jsonObj["event"]["user"];
  var word = new RegExp("^<@" + userId + ">.*");

  if(jsonObj["event"]["text"].match(word)) {
    return true;
  } else {
    return false;
  }
}

function SlackValidation(e) {
  var jsonObj = JSON.parse(e.postData.getDataAsString());

  // slackのchannelに参加した時のイベントを取り除く
  if(SlackJoinEvent(jsonObj)) {
    return false;
  }
  // observerの投稿は弾く
  if(jsonObj["event"]["user"] == "UUJQJ0YQG") {
    return false;
  }
  return jsonObj;
}

function SlackPost(channel, jsonObj, score) {
  // Slackの特定のチャンネルに投稿
  var token = PropertiesService.getScriptProperties().getProperty('SLACK_ACCESS_TOKEN');  
  var slackApp = SlackApp.create(token); //SlackApp インスタンスの取得
  
  // 投稿メッセージ生成
  var template_string = "【${time}】\nダジャレ：${joke}\n名前：${name}\n評価：${score}";
  var date = new Date(Number(jsonObj["event_time"])*1000); // Dateオブジェクト生成
  var date_string = Utilities.formatDate(date,"JST","yyyy/MM/dd HH:mm:ss");

  template_string = template_string.replace("${time}", date_string);
  template_string = template_string.replace("${joke}", jsonObj["event"]["text"]);
  template_string = template_string.replace("${name}", jsonObj["event"]["user"]);
  template_string = template_string.replace("${score}", score);

  var options = {
    channelId: channel, //チャンネル名
    userName: "obserber", //投稿するbotの名前
    //投稿するメッセージ
    message: template_string,
  };

  // 投稿
  slackApp.postMessage(options.channelId, options.message, {username: options.userName});
}

function test(jsonObj) {
  // ダジャレ判定APIにアクセス
  var isjoke = true;
  if(!isjoke) {
    return;
  }

  // ダジャレ評価APIにアクセス
  var score = 3.5;

  // #ついったーに投稿
  SlackPost("#ついったー", jsonObj, score);

  // スプレットシートに保存
  Slack2SheetPost(jsonObj, score);
}

function doPost(e) {
  var jsonObj = SlackValidation(e);
  if(jsonObj != false) {
    test(jsonObj);
  }
}
