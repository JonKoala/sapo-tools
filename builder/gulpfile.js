var gulp = require('gulp');
var child = require('child_process');
var git = require('gulp-git');
var install = require("gulp-install");
var open = require('gulp-open');

var fs = require('fs');
var configFile = fs.readFileSync('appconfig.json');
var appconfig = JSON.parse(configFile);

gulp.task('reset-api', done => {
  git.reset('origin/master', {args:'--hard', cwd: appconfig.path.api}, done);
});
gulp.task('reset-client', done => {
  git.reset('origin/master', {args:'--hard', cwd: appconfig.path.client}, done);
});

gulp.task('update-api', ['reset-api'],  done => {
  git.pull('origin', 'master', {cwd: appconfig.path.api}, done);
});
gulp.task('update-client', ['reset-client'],  done => {
  git.pull('origin', 'master', {cwd: appconfig.path.client}, done);
});

gulp.task('install-dependencies-api', ['update-api'], done => {
  gulp.src([appconfig.path.api+'package.json']).pipe(install(done));
});
gulp.task('install-dependencies-client', ['update-client'], done => {
  gulp.src([appconfig.path.client+'package.json', appconfig.path.client+'bower.json']).pipe(install(done));
});

gulp.task('start-api', ['install-dependencies-api'], done => {
  child.spawn('npm.cmd', ['start'], {cwd: appconfig.path.api}, (err, stdout, stderr) => {
    console.log(stdout);
    console.log(stderr);
    done(err);
  });
});
gulp.task('start-client', ['install-dependencies-client'], done => {
  child.spawn('npm.cmd', ['start'], {cwd: appconfig.path.client}, (err, stdout, stderr) => {
    console.log(stdout);
    console.log(stderr);
    done(err);
  });
});

gulp.task('open-browser', ['install-dependencies-api', 'install-dependencies-client'], done => {
  setTimeout(() => {
    gulp.src(__filename).pipe(open({uri: appconfig.url, app: 'chrome'}, done));
  }, 1000);
});

gulp.task('default', [
  'reset-api',
  'reset-client',
  'update-api',
  'update-client',
  'install-dependencies-api',
  'install-dependencies-client',
  'start-api',
  'start-client',
  'open-browser'
]);
