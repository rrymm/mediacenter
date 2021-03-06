<template>
    <div class="link-container">
        <template v-if="actions.details && instance.id">
            <div class="link post">
                <div class="post-header">
                    <div @click="showUserProfile(instance.content_item.owner.profile.id)" class="author">
                        <div class="profile-picture icon-container">
                            <img v-if="instance.content_item.owner.profile.picture" :src="instance.content_item.owner.profile.picture" />
                            <i v-if="!instance.content_item.owner.profile.picture" class="ion-md-person"></i>
                        </div>
                        <div class="author-details">
                            <span class="display-name">{{ instance.content_item.owner.profile.display_name }}</span>
                            <span class="user-title">User</span>
                        </div>
                    </div>
                    <div class="post-details">
                        <span class="title"><a :href="instance.link">{{ instance.content_item.title }}</a></span>
                        <span class="date">{{ instance.content_item.created.format('LLLL') }}</span>
                    </div>
                </div>
                <p class="text">
                    <a :href="instance.link">{{ instance.link }}</a><br />
                    <span v-if="instance.content_item.interests.length">Interests:</span>
                    <tag-list :tags="instance.content_item.interests" tagType="interest" /><br />
                    {{ instance.content_item.description }}
                </p>
                <div class="actions" v-if="isActiveUser">
                    <button type="button" @click="editLink">
                        <i class="ion-md-create"></i> Edit
                    </button>
                    <delete-button objectName="link" @delete="deleteLink" />
                </div>
            </div>
            <h2 class="align-left">Comments</h2>
            <router-view :contentObjectId="instance.content_item.id" />
        </template>
        <template v-if="actions.manage">
            <form class="main-form" @submit.prevent="save">
                <fieldset>
                    <label class="stack" for="title">Title</label>
                    <input v-model="instanceForm.content_item.title" type="text" name="title" placeholder="Link title" />
                    <label class="stack" for="title">Description</label>
                    <textarea class="stack" v-model="instanceForm.content_item.description" name="description" placeholder="Link description" />
                    <label class="stack" for="link">Link</label>
                    <input v-model="instanceForm.link" type="text" name="link" placeholder="https://example.com" />

                    <label class="stack" for="interests">Interests</label>
                    <interest-select v-model="instanceForm.content_item.interests" />

                    <label class="stack" for="places">Places</label>
                    <place-select v-model="instanceForm.content_item.places" />

                    <input type="submit" class="stack" value="Save changes" />
                </fieldset>
            </form>
        </template>
    </div>
</template>

<script>
import RestfulComponent from "./RestfulComponent"
import {activeUser, links, groups} from '../store.js'
//import {LinkModel} from '../models/Link.js'
import linkDeps from '../dependencies/Link.js'

import Comment from './Comment/Comment'
import InterestSelect from './InterestSelect'
import PlaceSelect from './PlaceSelect'
import TagList from './TagList'

import DeleteButton from './Gui/DeleteButton'

import router from "../router/index.js"

export default {
    name: 'hyperlink',
    mixins: [RestfulComponent],
    props: ['stashId', 'feedId'],
    components: {
        Comment,
        InterestSelect,
        PlaceSelect,
        TagList,
        DeleteButton
    },
    data() {
        return {
            objectName: 'link',
            isActiveUser: false,
            instanceForm: { content_item: {} }
        }
    },
    methods: {
        initialState() {
            this.instance = { id: null, content_item: { feeds: [] } }
            this.instanceForm = { content_item: { interests: [] } }
        },

        showUserProfile(id) {
            router.push(`/profile/${id}/details`)
        },

        editLink() {
            router.push(`../../manage`)
        },

        async manage(params) {
            const fallthrough = this.parentId ? `/link/${this.parentId}/details` : `/feed/list`

            this.instance = await this.showInstance(params.id, fallthrough, links, await linkDeps(this.stashId))

            this.instanceForm = this.instance.getForm()

            if (this.instance.content_item.interests.length === 0 && this.params && this.params.groupId) {
                const groupCollection = await groups()
                // Default to using Group's interests
                const group = await groupCollection.fetchInstance({id: parseInt(this.params.groupId)})
                this.instanceForm.content_item.interests = group.feed.interests.slice()
            }
        },

        async details(params) {
            if (!this.params.commentAction) {
                router.replace({
                    path: 'details/comment/list',
                    ...this.params
                })
            }

            this.instance = await this.showInstance(params.id, '/feed/list', links, await linkDeps(this.stashId))
            const user = await activeUser()
            this.isActiveUser = this.instance.content_item.owner.id === user.details.id
        },

        async deleteLink() {
            const linksCollection = await links()
            await linksCollection.destroy(this.instance, await linkDeps(this.stashId))
            router.replace('../../../..')
        },

        async manageLink() {
            const linksCollection = await links()
            return linksCollection.manage(this.instance, this.instanceForm, await linkDeps(this.stashId))
                .catch((error) => {
                    console.log(error)
                })
        },

        save() {
            if (this.actions.manage) {
                this.manageLink().then(() => {
                    router.push(`details`)
                })
            }
        }
    }
}
</script>

<style lang="scss">
.post-details {
    span.title a {
        color: white;
        text-decoration: underline;
    }
}
.link-container {
    height: calc(100vh - 60px);
    overflow: scroll;
    .post p.text {
        padding: 10px 20px
    }
}
</style>
