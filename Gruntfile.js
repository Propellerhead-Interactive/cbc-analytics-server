module.exports = function(grunt) {
     "use strict";
  var statsBanner = "/* lanaReadJS  <%= pkg.version %> */\n",
       hint_opts = {
        bitwise : false, //allow bit operand to generate id
        camelcase : false,
        curly : true,
        eqeqeq : true,
        es3 : false,
        forin : true,
        globals : { 
          "document" : true,
          "console" : true,
          "alert" : true,
          "window" : true,
          "escape" : true,
          "unescape" : true,
          "module" : true,
          "readJS" : true,
          "lana" : true
        },
        immed : false,
        indent : 4,
        latedef : true,
        maxdepth : 5,
        maxparams : 5,
        newcap : true,
        noarg : true,
        noempty : true,
        nonew : true,
        plusplus : false,
        quotmark : true,
        strict : true,
        trailing : true,
        undef : true,
        unused : false
    };
  var deployment = {
    src_folder: "./src/",
    build_folder:"./build/"
  };
  var config = {
    options: {},
    deployment: deployment,
    pkg: grunt.file.readJSON("package.json"),
   
    uglify: {
      options: {
        banner: statsBanner
      },
      dist: {
        files: {
          "build/js/lanaread.js": ["./lana.js", "./read.js", "./metadata.js"]
        }
      }
    },
    jshint: {
      files: ["Gruntfile.js", "./lana.js", "./read.js", "./metadata.js" ],
      options: hint_opts
    }
  };

  grunt.initConfig(config);
  grunt.loadNpmTasks("grunt-contrib-jshint");
  grunt.loadNpmTasks("grunt-contrib-uglify");

  grunt.registerTask("default", ["jshint", "uglify" ]);
    
};