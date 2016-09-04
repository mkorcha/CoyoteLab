var gulp     = require('gulp'),
    sass     = require('gulp-sass'),
    minicss  = require('gulp-clean-css'),
    uglify   = require('gulp-uglify'),
    concat   = require('gulp-concat')
;

var paths = {
	in: {
		js: [
			'node_modules/xterm/src/xterm.js', 
		    'res/js/**/*.js'
		],
		sass: [
			'node_modules/normalize.css/normalize.css',
			'node_modules/xterm/src/xterm.css',
			'res/sass/**/*.scss'
		],
		img: 'res/img/**/*'
	},
	out: {
		js:  'public/js',
		css: 'public/css',
		img: 'public/img'
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

gulp.task('img', function() {
	gulp.src(paths.in.img)
		.pipe(gulp.dest(paths.out.img));
});

gulp.task('default', ['sass', 'js', 'img'])
