const JUDGE_API_BASE_URL = "http://abelab.dev:8080";

function slack2SheetPost(jsonObj, score) {
  // スプレットシートに記述する
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('index');
  const newRow = sheet.getLastRow() + 1;

  sheet.getRange(newRow, 1).setValue(jsonObj["event_time"]); // タイムスタンプ
  sheet.getRange(newRow, 2).setValue(jsonObj["event_id"]); // イベントID
  sheet.getRange(newRow, 3).setValue(jsonObj["event"]["name"]); // ユーザーID
  sheet.getRange(newRow, 4).setValue(jsonObj["event"]["text"]); // 本文
  sheet.getRange(newRow, 5).setValue(score); // score
  sheet.getRange(newRow, 6).setValue(-1); // likes
  sheet.getRange(newRow, 7).setValue("Slack"); // slack or twitter
  const link = "https://dajarerits.slack.com/archives/" + jsonObj["event"]["channel"] + "/p";
  sheet.getRange(newRow, 8).setValue(link + jsonObj["event"]["ts"].replace('.','')); // link
  sheet.getRange(newRow, 9).setValue(""); // 備考
}

function regularExpressionJudge(jsonObj, word) {
  return jsonObj["event"]["text"].match(word);
}

function slackValidation(e) {
  const jsonObj = JSON.parse(e.postData.getDataAsString());

  // observerの投稿は弾く
  if(jsonObj["event"]["user"] == "UUJQJ0YQG") {
    return false;
  }

  // slackのchannelに参加した時のイベントを取り除く
  // この場合「<userid>~~~」という文字列がtextに入る
  const JoinWord = new RegExp("^<@" + jsonObj["event"]["user"] + ">.*");
  if(regularExpressionJudge(jsonObj, JoinWord)) {
    return false;
  }

  // slackのリアクションイベントは弾く
  // この場合「: ~~~~ :」という文字列がtextに入る
  const reactionwWord = new RegExp("^:.*:$");
  if(regularExpressionJudge(jsonObj, reactionwWord)) {
    return false;
  }
  
  // 前回のダジャレとイベントIDが一緒の時は弾く
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('index');
  const lastRow = sheet.getLastRow();
  const eventId = sheet.getRange(lastRow, 2).getValue();
  if(jsonObj["event_id"] == eventId) {
    return false;
  }

  // bottest,ダジャレチャンネル以外からのアクセスは弾く
  if(jsonObj["event"]["channel"] != "CTZKSMLCA" && jsonObj["event"]["channel"] != "CU8LLRTEV") {
    return false;
  }

  return jsonObj;
}

function slackPost(channel, jsonObj, evaluateScore) {
  // Slackの特定のチャンネルに投稿
  const token = PropertiesService.getScriptProperties().getProperty('SLACK_ACCESS_TOKEN');  
  const slackApp = SlackApp.create(token); //SlackApp インスタンスの取得
  
  // 投稿メッセージ生成
  const templateString = "【${time}】\nダジャレ：${joke}\n名前：${name}\n評価：${score}";
  const date = new Date(Number(jsonObj["event_time"])*1000); // Dateオブジェクト生成
  const dateString = Utilities.formatDate(date,"JST","yyyy/MM/dd HH:mm:ss");

  const message = templateString.replace("${time}", dateString)
                                 .replace("${joke}", jsonObj["event"]["text"])
                                 .replace("${name}", jsonObj["event"]["name"])
                                 .replace("${score}", evaluateScore);

  const options = {
    channelId: channel, // チャンネル名
    userName: "obserber", // 投稿するbotの名前
    // 投稿するメッセージ
    message: message,
  };

  // 投稿
  slackApp.postMessage(options.channelId, options.message, {username: options.userName});
}

function accessJudgeApi(joke, base_url) {
  const apiUrl = "/joke/judge/?joke=";
  const response = UrlFetchApp.fetch(base_url+ apiUrl + joke).getContentText();
  const resJson = JSON.parse(response);
  return resJson["is_joke"];
}

function accessEvaluateApi(joke, base_url) {
  const apiUrl = "/joke/evaluate/?joke=";
  const response = UrlFetchApp.fetch(base_url+ apiUrl + joke).getContentText();
  const resJson = JSON.parse(response);
  return Math.round(Number(resJson["score"]) * 10) / 10;
}

function iD2Name(id) {
  const token = PropertiesService.getScriptProperties().getProperty('SLACK_ACCESS_TOKEN');  
  const slackApp = SlackApp.create(token); //SlackApp インスタンスの取得
  const userinfo = slackApp.usersInfo(id);

  return userinfo["user"]["profile"]["display_name"];
}

function test(jsonObj) {

  const base_url = JUDGE_API_BASE_URL;

  // ダジャレ判定APIにアクセス
  //const isjoke = accessJudgeApi(jsonObj["event"]["text"], base_url);
  //if(!isjoke) {
  //  return;
  //}

  // ダジャレ評価APIにアクセス
  //const score = accessEvaluateApi(jsonObj["event"]["text"], base_url);
  const score = 10000; // ここあとでtry-catchしておく
  
  // ユーザーの表示名を追加
  jsonObj["event"]["name"] = iD2Name(jsonObj["event"]["user"]);
  
  // #ついったーに投稿
  const twitterScore = Math.round(score);
  slackPost("#ついったー", jsonObj, twitterScore);
  
  // スプレットシートに保存
  slack2SheetPost(jsonObj, score);
}

//function doPost(e) {
//  console.log("aaa");
//  let jsonObj = slackValidation(e);
//  if(jsonObj != false) {
//    test(jsonObj);
//  }
//}

function doPost(e){
  try{
    let jsonObj = slackValidation(e);
    if(jsonObj != false) {
      test(jsonObj);
    }
  }
  catch(o_O){
    console.log(o_O.message); throw o_O;
  }
}

const debug = () => {
  console.log(accessJudgeApi("布団がふっとん", JUDGE_API_BASE_URL))
}
