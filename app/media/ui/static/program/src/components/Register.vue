<template>
    <div>
        <info-box preErrorMessage="The account could not be created" :message="infoBoxMessage" :errorData="infoBoxErrorData" :status="infoBoxStatus" />

        <Modal :isOpen="isModalOpen" :onClose="closeModal" justifyContent="center" :titleProps="{ title: 'Register' }">
            <form id="register-form" @submit.prevent="register">
                <fieldset>
                    <legend>Details</legend>
                    <label class="stack" for="name">Username</label>
                    <input class="stack" v-model="instanceForm.username" type="text" placeholder="Username" required>
                    <label class="stack" for="name">Display Name</label>
                    <input class="stack" v-model="instanceForm.display_name" type="text" placeholder="Display Name" required>
                    <label class="stack" for="password">Password</label>
                    <input class="stack" v-model="instanceForm.password" id="password" type="password" placeholder="Password" required>
                    <!-- <label class="stack" for="retype-password">Re-type Password</label> -->
                    <!-- <input class="stack" v-model="instanceForm.retype_password" id="retype-password" type="password" placeholder="Password" required> -->
                    <label class="stack" for="email">Email Address</label>
                    <input class="stack" autocomplete="email" v-model="instanceForm.email" id="email" type="email" placeholder="Email Address" required>

                    <label class="stack" for="invite_code">Invite Code</label>
                    <input class="stack" v-model="instanceForm.invite_code" type="text" placeholder="Invite Code" required>

                    <label class="stack">
                        <input name="subscribe" class="stack" v-model="instanceForm.subscribe" id="subscribe" type="checkbox">
                        <span class="checkable">I wish to subscribe to the mailing list</span>
                    </label>

                    <!-- TODO must be over 13 -->
                    <input type="submit" class="stack" value="Submit" :disabled="registered" />
                </fieldset>
            </form>
        </Modal>
    </div>
</template>

<script>
import {AccountCollection} from '../models/Account.js'
import Modal from './Gui/Modal/Modal'
import InfoBox from './Gui/InfoBox'

export default {
    components: {
        Modal,
        InfoBox
    },
    data() {
        return {
            isModalOpen: true,
            infoBoxStatus: "",
            infoBoxMessage: "",
            infoBoxErrorData: {},
            instanceForm: {
                username: "",
                display_name: "",
                password: "",
                retype_password: "",
                email: "",
                subscribe: ""
            },
            registered: false
        }
    },
    computed: {
        info() {
            //return Your account was created successfully
            //return error, info
            return {
                alert: true,
                hidden: (this.infoBox.message.length < 1),
                error: (this.infoBox.status === "error"),
                info: (this.infoBox.status === "info"),
                success: (this.infoBox.status === "success")
            }
        }
    },
    methods: {
        closeModal() {
            this.isModalOpen = false
        },
        register() {
            this.registered = true
            AccountCollection.create({
                username: this.instanceForm.username,
                email: this.instanceForm.email,
                country: this.instanceForm.country,
                invite_code: this.instanceForm.invite_code,
                // display_name: this.instanceForm.display_name,
                password: this.instanceForm.password,
                profile: {
                    display_name: this.instanceForm.display_name
                },
                account_settings: {}
            })
                .then(() => {
                    this.infoBoxStatus = "success"
                    this.infoBoxMessage = 'Your account was successfully created. Please login.'
                    //this.router.navigate home
                })
                .catch(async (error) => {
                    this.registered = false
                    this.infoBoxStatus = "error"
                    this.infoBoxErrorData = await error.data
                })
            //"Please enter the following information below."
        }
    }
}
</script>

<style lang="scss">
#register-form {
    display: flex;
    align-self: center;
    width: 640px;
    fieldset {
        width: 100%;
    }
}
</style>
