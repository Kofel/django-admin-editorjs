document.addEventListener('DOMContentLoaded', function() {
    const editorContainers = document.querySelectorAll('[id^="editorjs-"]');
    
    editorContainers.forEach(container => {
        const inputId = container.id.replace('editorjs-', '');
        const inputField = document.getElementById(inputId);
        
        // Получаем начальные данные из скрытого поля
        let initialData = {};
        try {
            initialData = JSON.parse(inputField.value);
        } catch (e) {
            console.error('Failed to parse initial JSON data', e);
        }
        
        // Инициализируем Editor.js
        const editor = new EditorJS({
            holder: container.id,
            placeholder: 'Тут начинается текст новой статьи',
            logLevel: 'ERROR',
            tools: {
                header: {
                    class: Header,
                    inlineToolbar : true
                },
                list: {
                    class: EditorjsList,
                    inlineToolbar: true,
                    config: {
                        defaultStyle: 'unordered'
                    },
                },
                paragraph: {
                    class: Paragraph,
                    inlineToolbar: true
                },
                image: {
                    class: ImageTool,
                    config: {
                        uploader: {
                            uploadByFile(file) {
                                const postId = document.getElementById('id_post_id').value;
                                
                                if (!postId) {
                                    console.error('Post ID not found');
                                    return Promise.reject('Post ID not found');
                                }
                                
                                const formData = new FormData();
                                formData.append('image', file);
                                formData.append('post_id', postId);

                                return fetch('/admin/post-image-upload/', {
                                    method: 'POST',
                                    body: formData,
                                    headers: {
                                        'X-CSRFToken': getCookie('csrftoken')
                                    }
                                })
                                .then(response => response.json());
                            }
                        }
                    }
                },
                code: CodeTool,
                inlineCode: {
                    class: InlineCode,
                    inlineToolbar: true
                },
                table: Table,
                underline: Underline,
                raw: RawTool,
            },
            data: initialData,
            onReady: function() {
                console.log('Editor.js is ready to work!')
            },
            onChange: function() {
                editor.save().then(savedData => {
                    inputField.value = JSON.stringify(savedData);
                });
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}