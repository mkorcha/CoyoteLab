var gulp    = require('gulp'),
    sass    = require('gulp-sass'),
    minicss = require('gulp-clean-css'),
    uglify  = require('gulp-uglify'),
    concat  = require('gulp-concat')
;

var paths = {
	in: {
		js:   'res/js/**/*.js',
		sass: 'res/sass/**/*.scss'
	},
	out: {
		js:   'public/js',
		css:  'public/css'
	}
}

gulp.task('sass', function() {
	gulp.src(paths.in.sass)
	    .pipe(sass())
	    .pipe(minicss())
	    .pipe(gulp.dest(paths.out.css));
});

gulp.task('js', function() {
	gulp.src(paths.in.js)
	    .pipe(concat('main.js'))
	    .pipe(uglify())
	    .pipe(gulp.dest(paths.out.js));
});

gulp.task('default', ['sass', 'js'])
