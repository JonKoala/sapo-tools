var fs = require('fs');
var childProcess = require('child_process');
var path = require('path');
var ffmpeg = require('fluent-ffmpeg');


//CONSTANTS
var INPUT_FOLDER = 'input/';
var OUTPUT_FOLDER = 'output/';

//loading appconfig
var configFile = fs.readFileSync('appconfig.json');
var appconfig = JSON.parse(configFile);


function compressFile(fileName, inputRef, outputRef) {

  return new Promise((res, rej) => {
    var command = new ffmpeg();
    command.input(inputRef)
      .noAudio()
      .videoCodec(appconfig.codec)
      .videoBitrate(appconfig.bitrate)
      .output(outputRef)
      .on('end', res)
      .on('error', rej)
      .on('progress', progress => {
        console.log('processing ' + fileName + ' (' + parseInt(progress.percent) + '% done)')
      });
    command.run();
  });
}

function executeRoutineStep(files, index=0, report=null) {
  report = report || {success:[], failure:[]};
  if (files.length <= index) return report;
  var file = files[index];

  console.log('starting compression on ' + file + ' (' + (index+1) + '/' + files.length + ')');

  //call routine
  return compressFile(file, INPUT_FOLDER + file, OUTPUT_FOLDER + file)
    .then(() => {
      console.log('done compressing ' + file + '\n');
      report.success.push(file);
    }).catch(e => {
      console.log('failed compressing ' + file);
      console.log('error: ' + e.message + '\n');
      report.failure.push(file);
    }).then(() => {
      index++;
      return executeRoutineStep(files, index, report);
    });
}

function executeRoutine() {

  //getting files from input folder (except my .gitignore)
  var files = fs.readdirSync(INPUT_FOLDER)
    .filter(file => file !== '.gitignore');

  //creating output folder, if it doesn't exists
  if (!fs.existsSync(OUTPUT_FOLDER))
    fs.mkdirSync(OUTPUT_FOLDER);

  return Promise.resolve(executeRoutineStep(files));
}


//starting process
executeRoutine().then(report => {
  console.log('successfully compressed:', report.success.join(', ') || 'None');
  console.log('failed on compression:', report.failure.join(', ') || 'None');

  //opening outputs folder
  childProcess.exec('%SystemRoot%\\explorer.exe "' + path.join(__dirname, OUTPUT_FOLDER) + '"')
});
