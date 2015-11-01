var React = require('react');
var Dropzone = require('react-dropzone');
var superagent = require('superagent');

var Dz = React.createClass({
  getInitialState: function() {
    return {files: []}
  },

  componentDidMount: function(){
    this.setState({files: this.state.files})
  },

  onDrop: function(files) {
    //console.log('Received files: ', files);
    this.setState({files: files})
  },

  render: function() {
    return (
  	    <Dropzone onDrop={this.onDrop}>
          <div>Drop or click to attach your Job Description and Resumes here.</div>
        </Dropzone>
        <UploadFiles files={this.state.files} />
      </div>
    )
  }
});

var UploadFiles = React.createClass({
  onUpload: function(e) {
    e.preventDefault();
    //console.log(this.props.files);
    var files = this.props.files;
    /*
    var req = superagent.post('http://localhost:5000/upload');
    files.forEach((file)=> {
        req.attach("files", file, file.name);
    });
    req.end(function(err, res){
      console.log("err", err);
      console.log("res", res);
    });
    */
  },

  render: function() {
    return (
      <form onSubmit={this.onUpload}>
        <input type="submit" value="Upload Files" />
      </form>
    )
  }
});

var UploadBox = React.createClass({
  render: function() {
    return (
      <div>
        <div>CS3219 Project - CViA</div>
        <br />
        <Dz />
      </div>
    );
  }
});

React.render(
  <UploadBox />
  , document.getElementById('app')
);
