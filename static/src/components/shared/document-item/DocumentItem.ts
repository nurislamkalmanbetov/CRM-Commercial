import snackbar from "../snackbar/index";
import Loader from "../loader/index";
import Cookies from "js-cookie";

const API = {
  study_certificate: "/documents/study_certificate/",
  photo_for_schengen: "/documents/photo_for_schengen/",
  zagranpassport_copy: "/documents/zagranpassport_copy/",
  passport_copy: "/documents/passport_copy/",
  fluorography_express: "/documents/fluorography_express/",
  fluorography: "/documents/fluorography/",
  immatrikulation: "/documents/immatrikulation/",
  transcript: "/documents/transcript/",
  bank_statement: "/documents/bank_statement/",
  conduct_certificate: "/documents/conduct_certificate/",
  mentaldispanser_certificate: "/documents/mentaldispanser_certificate/",
  drugdispanser_certificate: "/documents/drugdispanser_certificate/",
  parental_permission: "/documents/parental_permission/",
  bank_details: "/documents/bank_details/",
  study_certificate_embassy: "/documents/study_certificate_embassy/",
  study_certificate_translate_embassy: "/documents/study_certificate_translate_embassy/",
  transcript_translate: "/documents/transcript_translate/"
};

export default class DocumentItem {
  wrapper: HTMLDivElement;
  fileInput: HTMLInputElement;
  api: string;
  close: HTMLDivElement;
  title: HTMLTitleElement;
  description: HTMLAnchorElement;
  content: HTMLDivElement;

  constructor(wrapper: HTMLDivElement) {
    const fileInput = wrapper.querySelector(".document-item__add") as HTMLInputElement;
    const api = wrapper.getAttribute("data-name") as string;
    const content = wrapper.querySelector(".document-item__content") as HTMLDivElement;
    const close = wrapper.querySelector(".document-item__close") as HTMLDivElement;
    const title = wrapper.querySelector(".document-item__title") as HTMLTitleElement;
    const description = wrapper.querySelector(".document-item__description") as HTMLAnchorElement;

    this.fileInput = fileInput;
    this.wrapper = wrapper;
    this.api = api;
    this.close = close;
    this.title = title;
    this.description = description;
    this.content = content;

    this.init();
  }

  private init() {
    if (this.fileInput) {
      this.fileInput.addEventListener("change", this.handleChange.bind(this));
    }
    if (this.close) {
      this.close.addEventListener("click", this.removeFile.bind(this));
    }
  }

  private handleChange(e: any) {
    const doc = e.target.files[0];
    const loader = new Loader();
    loader.show();
    this.sendDocument(doc)
      .then(res => {
        loader.remove();
        if (res.code === 200) {
          this.successAdd(res.document);
        } else {
          this.failureAdd();
        }
      })
      .catch(err => {
        loader.remove();
        this.failureAdd(err);
      });
  }

  sendDocument(doc: File) {
    const headers = new Headers();
    headers.append("X-CSRFToken", Cookies.get("csrftoken"));
    const formData = new FormData();
    formData.append("file", doc);
    return fetch(API[this.api], {
      method: "POST",
      body: formData,
      headers,
      credentials: "same-origin"
    }).then(res => res.json());
  }

  removeFile() {
    this.remove()
      .then(res => {
        if (res.code === 200) {
          this.successRemove();
        } else {
          this.failRemove();
        }
      })
      .catch(err => {
        this.failRemove();
      });
  }

  remove() {
    const headers = new Headers();
    headers.append("X-CSRFToken", Cookies.get("csrftoken"));
    return fetch(API[this.api], {
      method: "DELETE",
      headers,
      credentials: "same-origin"
    }).then(res => res.json());
  }

  successAdd(doc: { filename: string; url: string }) {
    const { filename, url } = doc;
    snackbar("Файл успешно добавлен", "success", 3000);
    this.wrapper.classList.add("document-item_success");
    if (this.description) {
      this.description.textContent =
        filename.length > 10 ? filename.substring(0, 9) + "..." : filename;
      this.description.href = url;
    } else {
      const description = document.createElement("a") as HTMLAnchorElement;
      description.className = "document-item__description document-item__description_link";
      description.textContent = filename.length > 25 ? filename.substring(0, 24) + "..." : filename;
      description.href = url;
      description.target = "_blank";
      this.content.appendChild(description);
      this.description = description;
    }
  }

  failureAdd(msg?: any) {
    snackbar(msg || "Что-то пошло не так :(", "danger", 3000);
  }

  successRemove() {
    snackbar("Файл успешно удален", "success", 3000);
    this.wrapper.classList.remove("document-item_success");
    this.title.textContent = this.title.getAttribute("data-title");
    this.description.textContent = "";
    this.description.href = "#";
  }

  failRemove() {
    snackbar("Не удалось удалить файл", "danger", 3000);
  }
}
