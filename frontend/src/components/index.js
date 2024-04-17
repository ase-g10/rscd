import FormGroupInput from "./Inputs/formGroupInput.vue";

import DropDown from "./Dropdown.vue";
import RSCDTable from "./RSCDTable.vue";
import Button from "./Button";

import Card from "./Cards/Card.vue";
import ChartCard from "./Cards/ChartCard.vue";
import StatsCard from "./Cards/StatsCard.vue";
import WebSocketNotifier  from "@/pages/Notifications/WebSocketNotifier";

import SidebarPlugin from "./SidebarPlugin/index";

let components = {
  FormGroupInput,
  Card,
  ChartCard,
  StatsCard,
  RSCDTable,
  DropDown,
  SidebarPlugin,
  WebSocketNotifier
};

export default components;

export {
  FormGroupInput,
  Card,
  ChartCard,
  StatsCard,
  RSCDTable,
  DropDown,
  Button,
  SidebarPlugin,
};
