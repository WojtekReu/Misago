import { MockedProvider } from "@apollo/react-testing"
import { actions } from "@storybook/addon-actions"
import React from "react"
import Navbar from "."
import { RootContainer, userFactory } from "../UI/Storybook"

export default {
  title: "Navbar",
}

const navbarActions = actions({
  openLogin: "open login",
  openRegister: "open register",
})

const settings = {
  forumName: "Misago",
}

export const Anonymous = () => (
  <MockedProvider>
    <RootContainer>
      <Navbar settings={settings} user={null} {...navbarActions} />
    </RootContainer>
  </MockedProvider>
)

export const Authenticated = () => (
  <MockedProvider>
    <RootContainer>
      <Navbar settings={settings} user={userFactory()} {...navbarActions} />
    </RootContainer>
  </MockedProvider>
)