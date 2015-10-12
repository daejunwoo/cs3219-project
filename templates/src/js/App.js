var React = require('react');
var Dropzone = require('react-dropzone');
var superagent = require('superagent');

var DropzoneDemo = React.createClass({
  onDrop: function(files) {
    console.log('Received files: ', files);
    this.setState({
      files: files
    });
  },

  render: function() {
    return (
	    <Dropzone onDrop={this.onDrop}>
        <div>Try dropping some files here, or click to select files to upload.</div>
      </Dropzone>
    );
  }
});

var UploadFiles = React.createClass({
  onUpload: function(e) {
    e.preventDefault();
    console.log("clicked upload");

    /* superagent stuff
      var req = superagent.post('/upload');
      files.forEach((file)=> {
          req.attach(file.name, file);
      });
      req.end(callback);
    */
  },

  render: function() {
    return (
      <form onSubmit={this.onUpload}>
        <input type="submit" value="Upload Files" />
      </form>
    );
  }
});

var UploadBox = React.createClass({
  render: function() {
    return (
      <div>
        <DropzoneDemo />
        <UploadFiles />
      </div>
    );
  }
});

React.render(
  <UploadBox />
  , document.getElementById('app')
);