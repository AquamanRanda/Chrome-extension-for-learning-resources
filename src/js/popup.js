import App from '../svelte/Popup.svelte';

const app = new App({
    target: document.body,
    props: {
        name: 'Learning Resorces Free/Paid'
    }
});

window.app = app;

export default app;