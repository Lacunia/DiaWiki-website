// The following are for profile.html. It helps with uploading pfp
document.getElementById('upload-btn').addEventListener('click', function() {
    console.log('Upload button clicked');
    // click the input element for choosing the pfp
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function() {
    console.log('File selected');
    document.getElementById('upload-form').submit();
});