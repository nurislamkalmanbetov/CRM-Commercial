document.addEventListener('DOMContentLoaded', () => {
    const itemTitles = document.querySelectorAll('.permissions-list__item-title-text');

    itemTitles.forEach(itm => itm.addEventListener('click', togglePermission));

    function togglePermission() {
        const parent = this.closest('.permissions-list__item');
        parent.classList.toggle('permissions-list__item_active');
    }

    const checkboxHandler = {
        init: () => {
            const parentElement = document.querySelectorAll('.parent-checkbox');
            const childElement = document.querySelectorAll('.child-checkbox');
            parentElement.forEach((el) => el.addEventListener('click', checkboxHandler.parentClick));
            childElement.forEach((el) => el.addEventListener('click', checkboxHandler.childClick));
        },
        parentClick: (e) => {
            const { target } = e;
            const parent = target.closest('.permissions-list__item');
            const childElements = parent.querySelectorAll('.child-checkbox');

            childElements.forEach((el) => {
                el.checked = target.checked;
            })
        },
        childClick: (e) => {
            const { target } = e;
            const parent = target.closest('.permissions-list__item');
            const childElements = parent.querySelectorAll('.child-checkbox');
            const parentCheckbox = parent.querySelector('.parent-checkbox');
            if(target.checked){
                parentCheckbox.checked = true;
            }
            let check = false;
            childElements.forEach(el => {
                if(el.checked) check = true;
            })
            if(!check) parentCheckbox.checked = false;
        },
        check: () => {
            const parents = document.querySelectorAll('.permissions-list__item');
            parents.forEach((parent) => {
                const children = parent.querySelectorAll('.child-checkbox');
                children.forEach((child) => {
                    if (child.checked){
                        const parentCheckbox = parent.querySelector('.parent-checkbox');
                        parentCheckbox.checked = true;
                        return;
                    }
                })
            })
        }
    };
    checkboxHandler.init();
    checkboxHandler.check();
});
