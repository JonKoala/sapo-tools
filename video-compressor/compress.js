var fs = require('fs');
var ffmpeg = require('fluent-ffmpeg');


var INPUT_FOLDER = 'inputs/';
var OUTPUT_FOLDER = 'outputs/';


function compressFile(fileName, inputRef, outputRef) {

  return new Promise((res, rej) => {
    var command = new ffmpeg();
    command.input(inputRef)
      .noAudio()
      .videoCodec('libx264')
      .videoBitrate('500k')
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

  var files = fs.readdirSync(INPUT_FOLDER)
  return Promise.resolve(executeRoutineStep(files))
}

executeRoutine().then(report => {
  console.log('successfully compressed:', report.success.join(', ') || 'None');
  console.log('failed on compression:', report.failure.join(', ') || 'None');
});
