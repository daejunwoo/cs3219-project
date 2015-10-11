var React = require('react');

var Parent = require('./Parent');
var Dropzone = require('react-dropzone');

var DropzoneDemo = React.createClass({
    onDrop: function (files) {
      console.log('Received files: ', files);
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

React.render(<div><Parent /><DropzoneDemo/></div>, document.getElementById('app'));