const LengthUnits = [{
    type: "category",
    text: "Metric:"
  },
  {
    type: "answer",
    text: "millimeter"
  },
  {
    type: "answer",
    text: "centimeter"
  },
  {
    type: "answer",
    text: "meter"
  },
  {
    type: "answer",
    text: "kilometer"
  },
  {
    type: "category",
    text: "Imperial:"
  },
  {
    type: "answer",
    text: "inch"
  },
  {
    type: "answer",
    text: "foot"
  },
  {
    type: "answer",
    text: "yard"
  },
  {
    type: "answer",
    text: "mile"
  },
  {
    type: "answer",
    text: "length of a football field"
  }
];

const TemperatureUnits = [{
    type: "answer",
    text: "celsius"
  },
  {
    type: "answer",
    text: "kelvin"
  },
  {
    type: "answer",
    text: "farenheit"
  }
];

const SpeedUnits = [{
    type: "answer",
    text: "kph"
  },
  {
    type: "answer",
    text: "mph"
  },
  {
    type: "answer",
    text: "m/s"
  }
];

const TimeUnits = [{
    type: "answer",
    text: "millisecond"
  },
  {
    type: "answer",
    text: "second"
  },
  {
    type: "answer",
    text: "minute"
  },
  {
    type: "answer",
    text: "hour"
  },
  {
    type: "answer",
    text: "day"
  },
  {
    type: "answer",
    text: "month"
  }
];

const MassUnits = [{
    type: "category",
    text: "Metric:"
  },
  {
    type: "answer",
    text: "milligram"
  },
  {
    type: "answer",
    text: "gram"
  },
  {
    type: "answer",
    text: "kilogram"
  },
  {
    type: "answer",
    text: "ton"
  },
  {
    type: "category",
    text: "Imperial:"
  },
  {
    type: "answer",
    text: "ounce"
  },
  {
    type: "answer",
    text: "pound"
  }
];

const VolumeUnits = [{
    type: "category",
    text: "Metric:"
  },
  {
    type: "answer",
    text: "milliliter"
  },
  {
    type: "answer",
    text: "liter"
  },
  {
    type: "answer",
    text: "cubic meter"
  },
  {
    type: "category",
    text: "Imperial:"
  },
  {
    type: "answer",
    text: "gallon"
  }
];

const ConversionFunctions = {
  // metric lengths
  millimeter: {
    centimeter: millimeters => millimeters / 10
  },
  centimeter: {
    millimeter: centimeters => centimeters * 10,
    meter: centimeters => centimeters / 100,
    inch: centimeters => centimeters / 2.54
  },
  meter: {
    centimeter: meters => meters * 100,
    kilometer: meters => meters / 1000
  },
  kilometer: {
    meter: kilometers => kilometers * 1000,
    mile: kilometers => kilometers * 0.62137
  },
  // imperial lengths
  inch: {
    centimeter: inches => inches * 2.54,
    foot: inches => inches / 12
  },
  foot: {
    inch: feet => feet * 12,
    yard: feet => feet / 3,
    "length of a football field": feet => feet / 360
  },
  yard: {
    foot: yards => yards * 3,
    mile: yards => yards / 1760
  },
  mile: {
    yard: miles => miles * 1760,
    kilometer: miles => miles * 1.609344
  },
  "length of a football field": {
    foot: fields => fields * 360
  },
  // temperatures
  celsius: {
    kelvin: celsius => celsius + 273.15
  },
  kelvin: {
    celsius: kelvin => kelvin - 273.15,
    farenheit: kelvin => 1.8 * (kelvin - 273.15) + 32
  },
  farenheit: {
    kelvin: farenheit => (farenheit - 32) * 1.8 + 273.15
  },
  // speed
  kph: {
    mph: kph => kph * 0.62137,
    "m/s": kph => kph / 3.6
  },
  "m/s": {
    kph: ms => ms * 3.6
  },
  mph: {
    kph: mph => mph / 0.62137
  },
  // time
  millisecond: {
    second: ms => ms / 1000
  },
  second: {
    millisecond: seconds => seconds * 1000,
    minute: seconds => seconds / 60
  },
  minute: {
    second: minutes => minutes * 60,
    hour: minutes => minutes / 60
  },
  hour: {
    minute: hours => hours * 60,
    day: hours => hours / 24
  },
  day: {
    hour: days => days * 24,
    month: days => days / 30
  },
  month: {
    day: months => months * 30
  },
  // metric mass
  milligram: {
    gram: milligrams => milligrams / 1000
  },
  gram: {
    milligram: grams => grams * 1000,
    kilogram: grams => grams / 1000
  },
  kilogram: {
    gram: kilograms => kilograms * 1000,
    ton: kilograms => kilograms / 1000,
    pound: kilograms => kilograms / 0.45359237
  },
  ton: {
    kilogram: tons => tons * 1000
  },
  // imperial mass
  ounce: {
    pound: ounces => ounces / 16
  },
  pound: {
    ounce: pounds => pounds * 16,
    kilogram: pounds => pounds * 0.45359237
  },
  // metric volume
  milliliter: {
    liter: milliliters => milliliters / 1000,
    gallon: milliliters => milliliters / 4546.09
  },
  liter: {
    milliliter: liters => liters * 1000,
    "cubic meter": liters => liters * 0.001
  },
  "cubic meter": {
    liter: meters => meters * 1000
  },
  // imperial volume
  gallon: {
    milliliter: gallons => gallons * 4546.09
  }
};

const SpecialPlurals = {
  foot: "feet",
  "length of a football field": "times the length of a football field",
  celsius: "degrees celsius",
  kelvin: "degrees kelvin",
  farenheit: "degrees farenheit"
};