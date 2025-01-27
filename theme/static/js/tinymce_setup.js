// static/js/tinymce_setup.js

import {init} from "../../../static_files/tinymce/tinymce";

init({
    selector: 'textarea',
    skin: 'oxide-dark',
    content_css: 'dark',
    plugins: 'advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount',
    toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help'
});
