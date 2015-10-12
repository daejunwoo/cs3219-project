var React = require('react');
var Dropzone = require('react-dropzone');

var DropzoneDemo = React.createClass({
    onDrop: function (files) {
      console.log('Received files: ', files);
      /*
        var req = request.post('/upload');
        files.forEach((file)=> {
            req.attach(file.name, file);
        });
        req.end(callback);
      */
    },

    render: function () {
      return (
      	<div>
			    <Dropzone onDrop={this.onDrop}>
            <div>Try dropping some files here, or click to select files to upload.</div>
          </Dropzone>
      	</div>
      );
    }
});

React.render(
  <div>
    <DropzoneDemo/>
  </div>,
  document.getElementById('app')
);