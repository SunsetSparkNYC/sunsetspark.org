module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: ['bower_components/foundation/scss']
      },
      dist: {
        options: {
          outputStyle: 'compressed'
        },
        files: {
          'css/app.css': 'scss/app.scss'
        }
      }
    },

    jade: {
      compile: {
        options: {
          data: {
            doctype: '5',
            debug: false,
            courses: grunt.file.readJSON('data/classes.json')
          }
        },
        files: {
          "index.html": ["jade/index.jade", ]
        }
      }
    },

    watch: {
      grunt: { files: ['Gruntfile.js'] },

      sass: {
        files: 'scss/**/*.scss',
        tasks: ['sass']
      },
      jade: {
        files: 'jade/**/*.jade',
        tasks: ['jade']
      }
    }
  });

  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-jade');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('build', ['sass']);
  grunt.registerTask('build', ['jade']);
  grunt.registerTask('default', ['build','watch']);
}
