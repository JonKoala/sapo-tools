var gulp = require('gulp');
var child = require('child_process');
var git = require('gulp-git');
var install = require("gulp-install");
var open = require('gulp-open');

var fs = require('fs');
var configFile = fs.readFileSync('appconfig.json');
var appconfig = JSON.parse(configFile);

gulp.task('update', (done) => {
  git.pull('origin', 'master', {cwd: appconfig.path.api}, done);
});

gulp.task('dependencies', ['update'], (done) => {
  gulp.src([appconfig.path.api+'package.json', appconfig.path.api+'bower.json']).pipe(install(done));
});

gulp.task('start', ['dependencies'], (done) => {
  child.spawn('npm.cmd', ['start'], {cwd: appconfig.path.api}, (err, stdout, stderr) => {
    console.log(stdout);
    console.log(stderr);
    done(err);
  });
});

gulp.task('open', ['dependencies'], (done) => {
  gulp.src(__filename).pipe(open({uri: appconfig.url}, done));
});

gulp.task('default', ['update', 'dependencies', 'start', 'open']);
