import "./styles/index.scss";

import {
  createPasswordInputs,
  createInputs,
  createCheckboxes,
  createForms,
  createFileInputs,
  createSelects,
  createSelectBand,
  createDateInputs
} from "./components/forms/index";

import { createWarningPopup, createQuestionnairePopup } from "./components/popups/index";

import {
  LOGIN_VALIDATION_SCHEMA,
  REGISTER_VALIDATION_SCHEMA,
  RESET_CODE_VALIDATION_SCHEMA,
  RESET_EMAIL_VALIDATION_SCHEMA,
  RESET_PASSWORD_VALIDATION_SCHEMA,
  BASIC_QUESTIONNAIRE_VALIDATION_SCHEMA
} from "./validations/index";

import { createReturnBtn, createDocumentItems, createPhotoLoader } from "./components/shared/index";



function init() {
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener("click", function(e) {
        e.preventDefault();

        const field = document.querySelector(this.getAttribute("href"));
        if (!field) return;
        field.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });

        field.focus();
      });
    });

    // for each input create Input class
    createInputs();

    createPhotoLoader();

    createWarningPopup();
    createQuestionnairePopup();

    //for each return btn items create ReturnBtn class
    createReturnBtn();

    //for each document item create DocumentItem class
    createDocumentItems();

    // for each file input created FileInput class
    createFileInputs();

    // for each input with type=password create InputPassword class
    createPasswordInputs();

    // for each checkbox input create Checkbox class
    createCheckboxes();

    // for each select input create Select class
    createSelects();

    createForms("#login", LOGIN_VALIDATION_SCHEMA);

    createForms("#register", REGISTER_VALIDATION_SCHEMA);

    createForms("#reset-email", RESET_EMAIL_VALIDATION_SCHEMA);

    createForms("#reset-password", RESET_PASSWORD_VALIDATION_SCHEMA);

    createForms("#reset-code", RESET_CODE_VALIDATION_SCHEMA);

    const form = createForms("#basic-questionnaire", BASIC_QUESTIONNAIRE_VALIDATION_SCHEMA);
    createSelectBand({
      parent: "birth_country",
      valueToShow: "Kirgisistan",
      children: ["birth_region", "birth_city"],
      form
    });

    createSelectBand({
      parent: "driver_license",
      valueToShow: "True",
      children: ["cat_a", "driving_experience", "transmission"],
      form
    });

    createDateInputs();
  });
}
// @ts-ignore: Unreachable code error
window.init = init;
