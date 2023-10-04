import Pikaday from 'pikaday';

export default () => {
  const DATE_INPUTS_QUERY = '[data-type="date"]';

  const inputs = document.querySelectorAll(DATE_INPUTS_QUERY) as NodeListOf<HTMLInputElement>;

  inputs.forEach(input => {
    new Pikaday({
      onSelect: (date) => {
      },
      format: 'DD-MM-YYYY',
      toString(date, format) {
        // you should do formatting based on the passed format,
        // but we will just return 'D/M/YYYY' for simplicity
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        const returnedDay = day < 10 ? `0${day}` : day;
        const returnedMonth = month < 10 ? `0${month}` : month;
        return `${returnedDay}-${returnedMonth}-${year}`;
      },
      parse(dateString, format) {
          // dateString is the result of `toString` method
          const parts = dateString.split('/');
          const day = parseInt(parts[0], 10);
          const month = parseInt(parts[1], 10) - 1;
          const year = parseInt(parts[2], 10);
          return new Date(year, month, day);
      },
      yearRange: [1970,2030],
      field: input,
      i18n: {
        previousMonth : 'Предыдущий месяц',
        nextMonth     : 'Следующий месяц',
        months        : ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        weekdays      : ['Воскресенье','Понедельник','Вторник','Среда','Четверг','Пятница','Суббота'],
        weekdaysShort : ['Вс','Пн','Вт','Ср','Чт','Пт','Сб']
    }
    })
  })
}